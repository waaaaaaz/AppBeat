# coding: utf-8

import time


class TimeUtils:
    LogFormat = "%Y%m%d-%H%M%S"
    OutputFormat = "%Y%m%d%H%M%S"

    @staticmethod
    def get_current_time_for_log():
        return time.strftime(TimeUtils.LogFormat, time.localtime(time.time()))

    @staticmethod
    def get_current_time_for_output():
        return time.strftime(TimeUtils.OutputFormat, time.localtime(time.time()))

    @staticmethod
    def get_current_time():
        return time.time()

    @staticmethod
    def duration(start_time):
        current_time = TimeUtils.get_current_time()
        duration = current_time - start_time
        return int(duration)

    @staticmethod
    def get_current_timestamp():
        return int(round(time.time() * 1000))

