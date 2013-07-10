__author__ = 'mathos'

from os.path import expanduser, expandvars
from configobj import ConfigObj

HOME = expanduser("~")
CONFIG_FILE = HOME+"/.pusher_man/pusher.conf"


def parse_configuration(config_file_path):
    """
    Returns a configuration dictionary parsed and validated by ConfigObj.
    @param config_file_path: The full path to the configuration file (required).
    @return: The parsed and validated configuration as a dictionary. Raises an IOError if the system is unable to read
    the configuration file.
    @raise ValidateError if the configuration file fails validation.
    """

    config = ConfigObj(config_file_path, file_error=True)

    def expand_path_variables(section, key):
        """
        Callback function used to expand path variables found in configuration values.
        @param section: The current section being processed
        @param key: The current key being processed
        @return: None
        """
        config_value = section[key]
        # we can only expand strings
        if isinstance(config_value, str) and '$' in config_value:
            section[key] = expandvars(config_value)

    # expand path variables - walk through all sections
    config.walk(expand_path_variables)

    return config