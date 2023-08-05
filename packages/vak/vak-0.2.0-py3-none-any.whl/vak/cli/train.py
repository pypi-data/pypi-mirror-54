from configparser import ConfigParser
import logging
import os
import pickle
import shutil
import sys
from datetime import datetime

import joblib
import numpy as np
import tensorflow as tf
from tqdm import tqdm

from ..dataset.classes import Dataset
from .. import network
from .. import utils
from ..utils.spect import SpectScaler


def train(train_vds_path,
          val_vds_path,
          networks,
          num_epochs,
          config_file,
          val_error_step=None,
          checkpoint_step=None,
          patience=None,
          save_only_single_checkpoint_file=True,
          normalize_spectrograms=False,
          root_results_dir=None,
          save_transformed_data=False,
          ):
    """train a single model using training set specified in config.ini file

    Parameters
    ----------
    train_vds_path : str
        path to Dataset that represents training data
    val_vds_path : str
        path to Dataset that represents validation data
    networks : dict
        where each key is the name of a neural network and the corresponding
        value is the configuration for that network (in a namedtuple or a dict)
    num_epochs : int
        number of training epochs. One epoch = one iteration through the entire
        training set.
    config_file : str
        path to config.ini file. Used to rewrite file with options determined by
        this function and needed for other functions (e.g. cli.summary)
    val_error_step : int
        step/epoch at which to estimate accuracy using validation set.
        Default is None, in which case no validation is done.
    checkpoint_step : int
        step/epoch at which to save to checkpoint file.
        Default is None, in which case checkpoint is only saved at the last epoch.
    patience : int
        number of epochs to wait without the error dropping before stopping the
        training. Default is None, in which case training continues for num_epochs
    save_only_single_checkpoint_file : bool
        if True, save only one checkpoint file instead of separate files every time
        we save. Default is True.
    normalize_spectrograms : bool
        if True, use spect.utils.data.SpectScaler to normalize the spectrograms.
        Normalization is done by subtracting off the mean for each frequency bin
        of the training set and then dividing by the std for that frequency bin.
        This same normalization is then applied to validation + test data.
    root_results_dir : str
        path in which to create results directory for this run of cli.learncurve
    save_transformed_data : bool
        if True, save transformed data (i.e. scaled, reshaped). The data can then
        be used on a subsequent run (e.g. if you want to compare results
        from different hyperparameters across the exact same training set).
        Also useful if you need to check what the data looks like when fed to networks.
        Default is False.

    Returns
    -------
    None

    Saves results in root_results_dir and adds some options to config_file.
    """
    # ---------------- pre-conditions ----------------------------------------------------------------------------------
    if val_error_step and val_vds_path is None:
        raise ValueError(
            f"val_error_step set to {val_error_step} but val_vds_path is None; please provide a path to "
            f"a validation data set that can be used to check error rate very {val_error_step} steps"
        )

    if val_vds_path and val_error_step is None:
        raise ValueError(
            "val_vds_path was provided but val_error_step is None; please provide a value for val_error_step"
        )

    timenow = datetime.now().strftime('%y%m%d_%H%M%S')
    if root_results_dir:
        results_dirname = os.path.join(root_results_dir,
                                       'results_' + timenow)
    else:
        results_dirname = os.path.join('.', 'results_' + timenow)
    os.makedirs(results_dirname)
    # copy config file into results dir now that we've made the dir
    shutil.copy(config_file, results_dirname)

    logfile_name = os.path.join(results_dirname,
                                'logfile_from_train_' + timenow + '.log')
    logger = logging.getLogger(__name__)
    logger.setLevel('INFO')
    logger.addHandler(logging.FileHandler(logfile_name))
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.info('Logging results to {}'.format(results_dirname))
    logger.info('Using config file: {}'.format(config_file))

    # ---------------- load training data  -----------------------------------------------------------------------------
    logger.info('Loading training Dataset from {}'.format(
        os.path.dirname(
            train_vds_path)))
    train_vds = Dataset.load(json_fname=train_vds_path)

    if train_vds.are_spects_loaded() is False:
        train_vds = train_vds.load_spects()

    X_train = train_vds.spects_list()
    X_train_spect_ID_vector = np.concatenate(
        [np.ones((spect.shape[-1],), dtype=np.int64) * ind for ind, spect in enumerate(X_train)]
    )
    X_train = np.concatenate(X_train, axis=1)

    Y_train = train_vds.lbl_tb_list()
    Y_train = np.concatenate(Y_train)

    if Y_train.ndim > 1:
        # not clear to me right why labeled_timebins get saved as (n, 1)
        # instead of as (n) vector--i.e. if another functions depends on that shape
        # Below is hackish way around figuring that out.
        Y_train = np.squeeze(Y_train)

    n_classes = len(train_vds.labelmap)
    logger.debug('n_classes: '.format(n_classes))

    timebin_dur = set([voc.metaspect.timebin_dur for voc in train_vds.voc_list])
    if len(timebin_dur) > 1:
        raise ValueError(
            f'found more than one time bin duration in training Dataset: {timebin_dur}'
        )
    elif len(timebin_dur) == 1:
        timebin_dur = timebin_dur.pop()
        logger.info('Size of each timebin in spectrogram, in seconds: {timebin_dur}')
    else:
        raise ValueError(
            f'invalid time bin durations from training set: {timebin_dur}'
        )

    X_train_dur = X_train.shape[-1] * timebin_dur
    logger.info(
        f'Total duration of training set (in s): {X_train_dur}'
    )

    # transpose X_train, so rows are timebins and columns are frequency bins
    # because networks expect this orientation for input
    X_train = X_train.T
    if save_transformed_data:
        joblib.dump(X_train, os.path.join(results_dirname, 'X_train'))
        joblib.dump(Y_train, os.path.join(results_dirname, 'Y_train'))

    # ---------------- load validation set (if there is one) -----------------------------------------------------------
    if val_vds_path:
        val_vds = Dataset.load(json_fname=val_vds_path)

        if val_vds.are_spects_loaded() is False:
            val_vds = val_vds.load_spects()

        if not val_vds.labelset == train_vds.labelset:
            raise ValueError(
                f'set of labels for validation set, {val_vds.labelset}, '
                f'does not match set for training set: {train_vds.labelset}'
            )

        X_val = val_vds.spects_list()
        X_val = np.concatenate(X_val, axis=1)

        Y_val = val_vds.lbl_tb_list()
        Y_val = np.concatenate(Y_val)

        timebin_dur_val = set([voc.metaspect.timebin_dur for voc in val_vds.voc_list])
        if len(timebin_dur_val) > 1:
            raise ValueError(
                f'found more than one time bin duration in validation Dataset: {timebin_dur_val}'
            )
        elif len(timebin_dur_val) == 1:
            timebin_dur_val = timebin_dur_val.pop()
            if timebin_dur_val != timebin_dur:
                raise ValueError(
                    f'time bin duration in validation Dataset, {timebin_dur_val}, did not match that of '
                    f'training set: {timebin_dur}'
                )

        X_val_dur = X_val.shape[-1] * timebin_dur
        logger.info(
            f'Total duration of validation set (in s): {X_val_dur}'
        )

        #####################################################
        # note that we 'transpose' the spectrogram          #
        # so that rows are time and columns are frequencies #
        #####################################################
        X_val = X_val.T
        if save_transformed_data:
            joblib.dump(X_val, os.path.join(results_dirname, 'X_val'))
            joblib.dump(Y_val, os.path.join(results_dirname, 'Y_val'))

        logger.info(
            f'will measure error on validation set every {val_error_step} steps of training'
        )
    else:
        X_val = None  # so we can just check 'if X_val' below, clearer than e.g. 'if X_val'

    logger.info(
        f'will save a checkpoint file every {checkpoint_step} steps of training'
    )

    if normalize_spectrograms:
        logger.info('will normalize spectrograms')
        spect_scaler = SpectScaler()
        X_train = spect_scaler.fit_transform(X_train)
        if X_val is not None:
            logger.info('normalizing validation set to match training set')
            X_val = spect_scaler.transform(X_val)
        joblib.dump(spect_scaler,
                    os.path.join(results_dirname, 'spect_scaler'))

    if save_transformed_data:
        scaled_data_filename = os.path.join(results_dirname,
                                            'scaled_spects')
        scaled_data_dict = {'X_train_scaled': X_train,
                            'Y_train_subset': Y_train}
        if X_val is not None:
            scaled_data_dict['X_val_scaled'] = X_val
        joblib.dump(scaled_data_dict, scaled_data_filename)

    freq_bins = X_train.shape[-1]  # number of columns
    logger.debug('freq_bins in spectrogram: '.format(freq_bins))

    NETWORKS = network._load()

    for net_name, net_config in networks.items():
        net_config_dict = net_config._asdict()
        net_config_dict['n_syllables'] = n_classes
        if 'freq_bins' in net_config_dict:
            net_config_dict['freq_bins'] = freq_bins
        net = NETWORKS[net_name](**net_config_dict)

        results_dirname_this_net = os.path.join(results_dirname, net_name)

        checkpoint_filename = f'checkpoint_{net_name}'
        checkpoint_path = os.path.join(results_dirname_this_net,
                                       checkpoint_filename)

        if not os.path.isdir(results_dirname_this_net):
            os.makedirs(results_dirname_this_net)
        logs_subdir = f'log_{net_name}'
        logs_path = os.path.join(results_dirname_this_net,
                                 'logs',
                                 logs_subdir)
        if not os.path.isdir(logs_path):
            os.makedirs(logs_path)

        net.add_summary_writer(logs_path=logs_path)

        if X_val is not None:
            (X_val_batch,
             Y_val_batch,
             num_batches_val) = utils.data.reshape_data_for_batching(X_val,
                                                                     net_config.batch_size,
                                                                     net_config.time_bins,
                                                                     Y_val)

        if save_transformed_data:
            scaled_reshaped_data_filename = os.path.join(results_dirname_this_net,
                                                         'scaled_reshaped_spects')
            scaled_reshaped_data_dict = {'X_train_scaled_reshaped': X_train,
                                         'Y_train_reshaped': Y_train,
                                         'X_val_scaled_batch': X_val_batch,
                                         'Y_val_batch': Y_val_batch}
            joblib.dump(scaled_reshaped_data_dict, scaled_reshaped_data_filename)

        costs = []
        val_errs = []
        curr_min_err = 1  # i.e. 100%
        err_patience_counter = 0

        with tf.Session(graph=net.graph) as sess:
            sess.run(net.init)

            # figure out number of batches we can get out of subset of training data
            # if we slide a window along the spectrogram with a stride of 1
            # and use each window as one sample in a batch
            num_timebins_training_set = X_train.shape[0]
            num_windows = num_timebins_training_set - net_config.time_bins
            logger.info('training set with {} time bins will yield {} windows '
                        'of width {} time bins'
                        .format(num_timebins_training_set,
                                num_windows,
                                net_config.time_bins))
            num_batches = num_windows // net_config.batch_size  # note floor division
            # meaning we'll throw away some windows
            new_last_ind = net_config.batch_size * num_batches
            logger.info('divided into batches of size {} yields {} batches '
                        'for a total of {} windows (throwing away {}).'
                        .format(net_config.batch_size,
                                num_batches,
                                new_last_ind,
                                num_windows - new_last_ind))

            for epoch in range(num_epochs):
                # every epoch we are going to shuffle the order in which we look at every window
                shuffle_order = np.random.permutation(num_windows)
                shuffle_order = shuffle_order[:new_last_ind].reshape(num_batches, net_config.batch_size)
                pbar = tqdm(shuffle_order)
                for batch_num, batch_inds in enumerate(pbar):
                    X_batch = []
                    Y_batch = []
                    for start_ind in batch_inds:
                        X_batch.append(
                            X_train[start_ind:start_ind + net_config.time_bins, :]
                        )
                        Y_batch.append(
                            Y_train[start_ind:start_ind + net_config.time_bins]
                        )
                    X_batch = np.stack(X_batch)
                    Y_batch = np.stack(Y_batch)
                    d = {net.X: X_batch,
                         net.y: Y_batch,
                         net.lng: [net_config.time_bins] * net_config.batch_size}
                    _cost, _, summary = sess.run((net.cost,
                                                  net.optimize,
                                                  net.merged_summary_op),
                                                 feed_dict=d)
                    costs.append(_cost)
                    net.summary_writer.add_summary(summary, epoch)
                    pbar.set_description(
                        f"epoch {epoch + 1}, batch {batch_num + 1} of {num_batches}, cost: {_cost:8.4f}"
                    )

                if val_error_step:
                    if epoch % val_error_step == 0:
                        if 'Y_pred_val' in locals():
                            del Y_pred_val

                        for b in range(num_batches_val):  # "b" is "batch number"
                            X_b = X_val_batch[:, b * net_config.time_bins: (b + 1) * net_config.time_bins, :]
                            Y_b = Y_val_batch[:, b * net_config.time_bins: (b + 1) * net_config.time_bins]
                            d = {net.X: X_b,
                                 net.y: Y_b,
                                 net.lng: [net_config.time_bins] * net_config.batch_size}

                            if 'Y_pred_val' in locals():
                                preds = sess.run(net.predict, feed_dict=d)
                                preds = preds.reshape(net_config.batch_size, -1)
                                Y_pred_val = np.concatenate((Y_pred_val, preds), axis=1)
                            else:
                                Y_pred_val = sess.run(net.predict, feed_dict=d)
                                Y_pred_val = Y_pred_val.reshape(net_config.batch_size, -1)

                        # get rid of zero padding predictions
                        Y_pred_val = Y_pred_val.ravel()[:Y_val.shape[0], np.newaxis]
                        val_errs.append(np.sum(Y_pred_val - Y_val != 0) / Y_val.shape[0])
                        print("epoch {}, validation error: {}".format(epoch + 1, val_errs[-1]))

                    if patience:
                        if val_errs[-1] < curr_min_err:
                            # error went down, set as new min and reset counter
                            curr_min_err = val_errs[-1]
                            err_patience_counter = 0
                            print("Validation error improved.\n"
                                  "Saving checkpoint to {}".format(checkpoint_path))
                            net.saver.save(sess, checkpoint_path)
                        else:
                            err_patience_counter += 1
                            if err_patience_counter > patience:
                                print("stopping because validation error has not improved in {} epochs"
                                      .format(patience))
                                with open(os.path.join(results_dirname_this_net, "costs"), 'wb') as costs_file:
                                    pickle.dump(costs, costs_file)
                                with open(os.path.join(results_dirname_this_net, "val_errs"), 'wb') as val_errs_file:
                                    pickle.dump(val_errs, val_errs_file)
                                break

                if checkpoint_step:
                    if epoch % checkpoint_step == 0:
                        "Saving checkpoint."
                        if save_only_single_checkpoint_file is False:
                            checkpoint_path_tmp = checkpoint_path + '_{}'.format(epoch)
                        else:
                            checkpoint_path_tmp = checkpoint_path
                        net.saver.save(sess, checkpoint_path_tmp)
                        with open(os.path.join(results_dirname_this_net, "val_errs"), 'wb') as val_errs_file:
                            pickle.dump(val_errs, val_errs_file)

                if epoch == (num_epochs - 1):  # if this is the last epoch
                    "Reached max. number of epochs, saving checkpoint."
                    net.saver.save(sess, checkpoint_path)
                    with open(os.path.join(results_dirname_this_net, "costs"),
                              'wb') as costs_file:
                        pickle.dump(costs, costs_file)
                    with open(os.path.join(results_dirname_this_net, "val_errs"),
                              'wb') as val_errs_file:
                        pickle.dump(val_errs, val_errs_file)

    # lastly rewrite config file,
    # so that paths where results were saved are automatically in config
    config = ConfigParser()
    config.read(config_file)
    config.set(section='OUTPUT',
               option='results_dir_made_by_main_script',
               value=results_dirname)
    with open(config_file, 'w') as config_file_rewrite:
        config.write(config_file_rewrite)
