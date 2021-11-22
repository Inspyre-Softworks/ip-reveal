from pathlib import Path

from configparser import ConfigParser
from inspy_logger import InspyLogger


muted = None
args = None

#
# class Config(object):
#     DEFAULT_CONF_FILEPATH = Path("~/Inspyre-Softworks/IP-Reveal/config/config.ini").expanduser()
#
#     FLAGFILE_PATH = Path(__file__).resolve().joinpath('flag.ini')
#
#     ARGS = parse()
#
#     ISL = InspyLogger()
#
#     PROG_LOG_NAME = 'IPReveal'
#
#     LOG_NAME = PROG_LOG_NAME + '.config'
#
#     ISL_DEV = ISL.LogDevice(PROG_LOG_NAME, ARGS.log_level)
#
#     PROG_LOG = ISL_DEV.start()
#     PROG_LOG.debug('Root logger started')
#
#     file_path = DEFAULT_CONF_FILEPATH
#
#     if not file_path.exists():
#         flag_file_fp = FLAGFILE_PATH
#         if not flag_file_fp.exists():
#             file_path = None
#             flag_file_fp = None
#         else:
#             pass
#             # TODO:
#             #     - Write code that does someting if the flag-file exists.
#             #         - Load path to actual config from this flag-file
#     else:
#         parser = ConfigParser()
#         parser.read(DEFAULT_CONF_FILEPATH)
#
#     """
#
#     (pathlib.Path)
#
#     If this program creates and stores a  'config.ini' file in any location except for `DEFAULT_CONF_FILEPATH` we
#     will create a simple .ini file at `FLAGFILE_PATH` to let the program know where to look for it's preferences when it
#     starts each time after it being assigned.
#
#     """
