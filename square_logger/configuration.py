import os

from lapa_commons.main import read_configuration_from_file_path

config_file_path = (
    os.path.dirname(os.path.abspath(__file__)) + os.sep + "data" + os.sep + "config.ini"
)
ldict_configurations = read_configuration_from_file_path(config_file_path)

# get all vars and typecast
cint_log_level = int(ldict_configurations["ENVIRONMENT"]["LOG_LEVEL"])
cstr_log_path = ldict_configurations["ENVIRONMENT"]["LOG_PATH"]
