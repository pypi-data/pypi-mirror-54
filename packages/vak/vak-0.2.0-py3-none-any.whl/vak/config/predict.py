"""parses [PREDICT] section of config"""
from configparser import NoOptionError
import os

import attr
from attr.validators import instance_of, optional

from .validators import is_a_directory, is_a_file
from .. import network


@attr.s
class PredictConfig:
    """class that represents [PREDICT] section of config.ini file

    Attributes
    ----------
    predict_vds_path : str
        path to saved Dataset that contains data for which annotations
        should be predicted.
    train_vds_path : str
        path to Dataset that represents training data.
        To fetch labelmap used during training, to map labels used
        in annotation to a series of consecutive integers that become
        outputs of the neural network. Used here to convert
        back to labels used in annotation.
    checkpoint_path : str
        path to directory with checkpoint files saved by Tensorflow, to reload model
    networks : namedtuple
        where each field is the Config tuple for a neural network and the name
        of that field is the name of the class that represents the network.
    spect_scaler_path : str
        path to a saved SpectScaler object used to normalize spectrograms.
        If spectrograms were normalized and this is not provided, will give
        incorrect results.
    """
    predict_vds_path = attr.ib(validator=[instance_of(str), is_a_file])
    train_vds_path = attr.ib(validator=[instance_of(str), is_a_file])
    checkpoint_path = attr.ib(validator=[instance_of(str), is_a_directory])
    networks = attr.ib()

    spect_scaler_path = attr.ib(validator=optional([instance_of(str), is_a_file]),
                                default=None)


def parse_predict_config(config):
    """parse [PREDICT] section of config.ini file

    Parameters
    ----------
    config : ConfigParser
        containing config.ini file already loaded by parse function

    Returns
    -------
    predict_config : vak.config.predict.PredictConfig
        instance of PredictConfig class that represents [PREDICT] section
        of config.ini file
    """
    config_dict = {}

    try:
        config_dict['predict_vds_path'] = os.path.expanduser(
            config['PREDICT']['predict_vds_path']
        )
    except KeyError:
        raise KeyError("'predict_vds_path' option not found in [PREDICT] section of "
                            "config.ini file. Please add this option.")
    try:
        config_dict['train_vds_path'] = os.path.expanduser(
            config['PREDICT']['train_vds_path']
        )
    except KeyError:
        raise KeyError("'train_vds_path' option not found in [PREDICT] section of "
                            "config.ini file. Please add this option.")

    try:
        config_dict['checkpoint_path'] = config['PREDICT']['checkpoint_path']
    except KeyError:
        raise KeyError('must specify checkpoint_path in [PREDICT] section '
                       'of config.ini file')

    # load entry points within function, not at module level,
    # to avoid circular dependencies
    # (user would be unable to import networks in other packages
    # that subclass vak.network.AbstractVakNetwork
    # since the module in the other package would need to `import vak`)
    NETWORKS = network._load()
    NETWORK_NAMES = NETWORKS.keys()
    try:
        networks = [network_name for network_name in
                    config['PREDICT']['networks'].split(',')]
        for network_name in networks:
            if network_name not in NETWORK_NAMES:
                raise TypeError('Neural network {} not found when importing installed networks.'
                                .format(network))
        config_dict['networks'] = networks
    except NoOptionError:
        raise KeyError("'networks' option not found in [PREDICT] section of config.ini file. "
                       "Please add this option as a comma-separated list of neural network names, e.g.:\n"
                       "networks = TweetyNet, GRUnet, convnet")

    if config.has_option('PREDICT', 'spect_scaler_path'):
        config_dict['spect_scaler_path'] = config['PREDICT']['spect_scaler_path']

    return PredictConfig(**config_dict)
