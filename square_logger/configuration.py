import configparser
import os

config = configparser.ConfigParser()
config_file_path = (
    os.path.dirname(os.path.abspath(__file__)) + os.sep + "data" + os.sep + "config.ini"
)
config.read(config_file_path)


# get all vars and typecast
cint_log_level = config.getint("ENVIRONMENT", "LOG_LEVEL")
cstr_log_path = config.get("ENVIRONMENT", "LOG_PATH")
