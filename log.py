# coding: utf-8

import os
import logging
from logging.handlers import RotatingFileHandler

from utils import FileUtils, TimeUtils
from setting import PROJECT_PATH


class Log(object):
    # Define logfile directory
    log_dir = os.path.join(PROJECT_PATH, "logs")

    # Define default logfile format.

    file_name_format = TimeUtils.get_current_time_for_log()
    console_msg_format = '%(asctime)s %(levelname)-8s: %(message)s'
    file_msg_format = '%(asctime)s %(levelname)-8s: %(message)s'
    # file_msg_format = '%(asctime)s %(levelname)-8s: %(module)-2s:%(funcName)-2s: %(process)-2d: %(processName)-2s:  %(name)s \n%(message)s'
    # console_msg_format = '%(asctime)s %(levelname)-8s: %(module)-2s:%(funcName)-2s: %(process)-2d: %(processName)-2s:  %(name)s \n%(message)s'

    # Define the log level
    log_level = logging.INFO

    # Define the log rotation criteria.
    # max_bytes = 1024 ** 2
    # backup_count = 100

    @staticmethod
    def logger(logger_name=None):
        # Create the root logger.
        logger = logging.getLogger(logger_name)
        logger.setLevel(Log.log_level)

        # Validate the given directory.
        Log.log_dir = os.path.normpath(Log.log_dir)

        # Create a folder for the logfile.
        FileUtils.make_dir(Log.log_dir)

        # Build the logfile name
        filename = Log.file_name_format + ".log"
        filename = os.path.join(Log.log_dir, filename)

        # Set up logging to the logfile
        file_handler = RotatingFileHandler(
            filename=filename
            # ,maxBytes=Log.max_bytes, backupCount=Log.backup_count
        )
        file_handler.setLevel(Log.log_level)
        file_formatter = logging.Formatter(Log.file_msg_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Set up logging to console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(Log.log_level)
        stream_formatter = logging.Formatter(Log.console_msg_format)
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        return logger
