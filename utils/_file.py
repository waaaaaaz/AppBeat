# coding: utf-8

import os
from shutil import copyfile
import pickle

from setting import PROJECT_PATH
from ._time import TimeUtils


class FileUtils:

    @staticmethod
    def make_dir(_dir):
        if not os.path.exists(_dir):
            os.makedirs(_dir)

    @staticmethod
    def rename_file(file_name, new_file_name):
        os.rename(file_name, new_file_name)

    @staticmethod
    def rename_and_copy_crash_pic(udid, file_name):
        new_file_name = file_name.replace(".png", "_crash.png")
        FileUtils.rename_file(file_name, new_file_name)
        FileUtils.copy_crash_pic(udid, file_name)

    @staticmethod
    def copy_file(src, dst):
        copyfile(src, dst)

    @staticmethod
    def copy_crash_pic(udid, file_name):
        crash_dir = FileUtils.crash_dir(udid)
        shot_file_name = file_name.split(os.pathsep)[:-1]
        dst_full_file_name = os.path.join(crash_dir, shot_file_name)
        FileUtils.copy_file(file_name, dst_full_file_name)

    @staticmethod
    def output_dir(udid, exe_id):
        output_dir = os.path.join(PROJECT_PATH, "output")
        device_name = udid.replace(":", "_")
        output_dir = os.path.join(output_dir, "{0}_{1}".format(device_name, exe_id))
        FileUtils.make_dir(output_dir)
        return output_dir

    @staticmethod
    def cache_dir(udid, exe_id):
        # output_dir = os.path.join(PROJECT_PATH, "local_cache")
        # device_name = udid.replace(":", "_")
        # output_dir = os.path.join(output_dir, "{0}_{1}".format(device_name, exe_id))
        cache_dir = os.path.join(FileUtils.output_dir(udid, exe_id), "local_cache")
        FileUtils.make_dir(cache_dir)
        return cache_dir

    @staticmethod
    def base_dir():
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def screen_shot_dir(udid, exe_id):
        screen_shot_dir = os.path.join(FileUtils.output_dir(udid, exe_id), "screen_shot")
        FileUtils.make_dir(screen_shot_dir)
        return screen_shot_dir

    @staticmethod
    def crash_dir(udid, exe_id):
        crash_dir = os.path.join(FileUtils.output_dir(udid, exe_id), "crash")
        FileUtils.make_dir(crash_dir)
        return crash_dir

    @staticmethod
    def device_log_dir(udid):
        device_log_dir = os.path.join(FileUtils.output_dir(udid), "device_log")
        FileUtils.make_dir(device_log_dir)
        return device_log_dir

    @staticmethod
    def file_available(file_path):
        return os.path.exists(file_path)

    @staticmethod
    def add_to_pickle(add_file_path, item):
        with open(add_file_path, 'ab') as _file:
            pickle.dump(item, _file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def read_pickle(read_file_path):
        if os.path.exists(read_file_path):
            with open(read_file_path, 'rb') as _file:
                try:
                    while True:
                        yield pickle.load(_file)
                except EOFError:
                    pass
        else:
            raise IOError('the file [{}] is not exist!'.format(read_file_path))

    @staticmethod
    def read_pickle_lines(read_file_path):
        lines = FileUtils.read_pickle(read_file_path)
        if getattr(lines, '__iter__', None):
            return lines
        else:
            raise IOError('unknown error for read lines.')

# if __name__ == "__main__":
#     # a = {"asd": "asd"}
#     b = {"123": "123"}
#     udid = "123123123"
#     cache_dir = PROJECT_PATH
#     file_name = cache_dir + os.path.sep + "{0}.pickle".format("aaaa")
#     FileUtils.add_to_pickle(file_name, b)
#     lines = FileUtils.read_pickle_lines(file_name)
#     for i in lines:
#         print (i)
