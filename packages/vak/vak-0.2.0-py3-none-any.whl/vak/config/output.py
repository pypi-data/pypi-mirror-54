"""parses [OUTPUT] section of config"""
import os
from configparser import NoOptionError

import attr
from attr.validators import optional

from .validators import is_a_directory


@attr.s
class OutputConfig:
    """class that represents [OUTPUT] section of config.ini file

    Attributes
    ----------
    root_results_dir : str
        directory in which results *will* be created.
        The vak.cli.learcurve function will create
        a subdirectory in this directory each time it runs.
    results_dirname : str
        name of subdirectory created by vak.cli.learncurve.
        This option is added programatically by that function
        when it runs but can be changed (e.g. to run
        vak.cli.summary on previous outputs of learncurve.)
    """
    root_results_dir = attr.ib(validator=optional(is_a_directory), default=None)
    results_dirname = attr.ib(validator=optional(is_a_directory), default=None)


def parse_output_config(config):
    """parse [OUTPUT] section of config.ini file

    Parameters
    ----------
    config : ConfigParser
        containing config.ini file already loaded by parse function

    Returns
    -------
    output_config : namedtuple
    """
    try:
        root_results_dir = config['OUTPUT']['root_results_dir']
        root_results_dir = os.path.expanduser(root_results_dir)
    except NoOptionError:
        raise KeyError('must specify root_results_dir in [OUTPUT] section '
                       'of config.ini file')

    if config.has_option('OUTPUT', 'results_dir_made_by_main_script'):
        # don't check whether it exists because it may not yet,
        # depending on which function we are calling.
        # So it's up to calling function to check for existence of directory
        results_dirname = config['OUTPUT']['results_dir_made_by_main_script']
        results_dirname = os.path.expanduser(results_dirname)
    else:
        results_dirname = None

    return OutputConfig(root_results_dir,
                        results_dirname)
