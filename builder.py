# coding: utf-8

import os

from rule import Rule
from flow import *
from driver import *
from utils import TimeUtils, VideoUtils, FileUtils
from log import Log
from exception import UDIDError, ElementFoundError
from setting import RecordsStatus

logger = Log.logger(__file__)


class Builder(object):

    def __init__(self, device_type, udid, mode, config_file):
        self.device_type = device_type
        self.udid = udid
        self.__udid_validate()
        self.mode = mode
        self.config_file = config_file
        self.exe_id = TimeUtils.get_current_time_for_output()
        self.start_time = TimeUtils.get_current_time()
        self.rule = self.__rule()
        self.driver = self.__driver_router()
        self.flow = self.__flow_router()
        self.cache_file_name = self.__cache_file_name()
        self.window_info = self.driver.window_info

    def __rule(self):
        return Rule(config_file=self.config_file, mode=self.mode, device_type=self.device_type, udid=self.udid,
                    exe_id=self.exe_id)

    def __driver_router(self):
        device_type_name = self.device_type.upper()
        class_name = device_type_name + "Driver"
        klass = globals()[class_name]
        return klass(self.rule)

    def __flow_router(self):
        execution_mode_name = self.mode.upper()
        class_name = execution_mode_name + "Model"
        klass = globals()[class_name]
        return klass(self.driver)

    def exe(self):
        while self.flow.action_count < self.rule.MAX_ACTION_COUNT_OPTIONAL and TimeUtils.duration(
                self.start_time) < self.rule.MAX_EXE_DURATION_OPTIONAL:
            try:
                self.flow.exe()
                # 所有执行记录在内存中, 防止过大, 将部分记录在本地缓存中
                if self.flow.action_count % 100 == 0:
                    self.to_local_cache()
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt caught. Program Stopped Manually")
                logger.info("DONE")
                self.to_local_cache()
                self.video_generator()
                break
            # 用于target模式
            except ElementFoundError:
                logger.info("target settings for xpath is incorrect. BREAK!!!")
                break
            except Exception as e:
                logger.error("error type is {0}".format(e.__class__.__name__))
                logger.error("error message is {0}".format(e))
                pass
        self.to_local_cache()
        self.video_generator()
        logger.info("DONE")

    def __udid_validate(self):
        if self.device_type == "android" and len(self.udid) >= 20:
            raise UDIDError("illegal udid : {0}; android udid length less than 20".format(self.udid))
        if self.device_type == "ios" and len(self.udid) < 20:
            raise UDIDError("illegal udid : {0} ios udid length more than 20".format(self.udid))

    def video_generator(self):
        logger.info("start to generate video")
        logger.info(self.window_info)
        height = self.window_info[1]
        weight = self.window_info[2]
        display = (height, weight)
        pic_dir = self.driver.screen_shot_dir
        logger.info("video start")
        video_name = VideoUtils.pic_to_video(pic_dir, display, self.exe_id)
        logger.info("video end")
        logger.info("video generated : {0}".format(video_name))

    def to_local_cache(self):
        if self.mode == "monkey":
            return
        for record in list(self.flow.exe_records.keys()):
            if self.flow.exe_records[record]["status"] == RecordsStatus.DONE:
                FileUtils.add_to_pickle(self.cache_file_name, self.flow.exe_records[record])
                for k in list(self.flow.exe_records[record].keys()):
                    if k != "status":
                        del self.flow.exe_records[record][k]

    def __cache_file_name(self):
        cache_dir = FileUtils.cache_dir(self.udid, self.exe_id)
        return cache_dir + os.path.sep + "{0}.pickle".format(self.exe_id)
