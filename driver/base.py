# coding: utf-8

from abc import abstractmethod, ABCMeta
import time
import os
import cv2

from log import Log
from utils import FileUtils, TimeUtils
from setting import APPIUM_NEW_COMMAND_TIMEOUT, APPIUM_SERVER_IP, APPIUM_SERVER_PORT, \
    DEFAULT_WAITING_DURATION_AS_SECOND, DEFAULT_WAITING_DURATION_AS_MILLISECOND
from exception import ElementFoundError

logger = Log.logger(__file__)


class Base(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, rule):
        self.udid = rule.udid
        self.mode = rule.mode
        self.exe_id = rule.exe_id
        self.screen_shot_dir = FileUtils.screen_shot_dir(self.udid, self.exe_id)

    @abstractmethod
    def driver(self):
        raise NotImplementedError

    def common_driver_prepare(self):
        caps = {
            "deviceName": self.udid,
            "udid": self.udid,
            "newCommandTimeout": APPIUM_NEW_COMMAND_TIMEOUT,
            "noReset": True
        }
        url = "http://{0}:{1}/wd/hub".format(APPIUM_SERVER_IP, APPIUM_SERVER_PORT)
        logger.info("info : appium url :: {0}".format(url))

        return url, caps

    def click_element(self, element):
        self.driver.click(element)

    def window_info(self):
        window_size = self.driver.get_window_size()
        window_height = window_size["height"]
        window_width = window_size["width"]
        logger.info("action : current window size is : {0}".format(window_size))
        logger.info("action : current window height is : {0}".format(window_height))
        logger.info("action : current window height is : {0}".format(window_width))
        return window_size, window_height, window_width

    def click_by_coordinate(self, position):
        logger.info("action : click by coordinate: x is {0}, y is {1}".format(position[0], position[1]))

        try:
            pic = self.take_screenshot()
            self.draw_circle(position, pic)
            self.driver.tap([position])
            # self.take_screenshot()
        except:
            pass

    def double_click_by_coordinate(self, position, duration=200):
        # duration, 毫秒
        logger.info("action: double click by coordinate")

        pic = self.take_screenshot()
        self.draw_circle(position, pic)

        coordinate = [position]
        self.driver.tap(coordinate, duration=duration).tap(coordinate)

    def long_press_by_coordinate(self, position):
        # duration, 毫秒
        logger.info("action: long press by coordinate")

        pic = self.take_screenshot()
        self.draw_circle(position, pic)

        coordinate = [position]
        self.driver.tap(coordinate, duration=200)

    def sleep(self, seconds=DEFAULT_WAITING_DURATION_AS_SECOND):
        # second
        logger.info("action : waiting for {0} seconds".format(seconds))
        time.sleep(seconds)

    def swipe(self, start_x, start_y, end_x, end_y, duration=DEFAULT_WAITING_DURATION_AS_MILLISECOND):
        # duration 毫秒, ms
        logger.info("action : swipe : start_x ==> {0}, start_y ==> {1}, end_x ==> {2}, end_y ==> {3}".format(
            start_x, start_y, end_x, end_y))
        self.driver.swipe(start_x, start_y, end_x, end_y, duration=duration)

    def swipe_up_default(self):
        logger.info("action: swipe up as default")

        height = self.window_info[1]
        weight = self.window_info[2]

        # 起点横坐标为屏幕中点, 纵坐标为屏幕下方三分之一
        start_x = int(weight * 0.5)
        start_y = int(height * 2 / 3)

        # 终点横坐标为屏幕中点(与起点横坐标一致), 纵坐标为屏幕上方三分之一
        end_x = start_x
        end_y = int(height / 3)
        logger.info("action : prepare to swipe up")
        self.swipe(start_x, start_y, end_x, end_y)
        self.sleep(1)

    def swipe_down_default(self):
        logger.info("action: swipe down as default")

        height = self.window_info[1]
        weight = self.window_info[2]

        # 起点横坐标为屏幕中点, 纵坐标为屏幕上方三分之一
        start_x = int(weight * 0.5)
        start_y = int(height / 3)

        # 终点横坐标为屏幕中点(与起点横坐标一致), 纵坐标为屏幕下方三分之一
        end_x = start_x
        end_y = int(height * 2 / 3)
        logger.info("action : prepare to swipe down")
        self.swipe(start_x, start_y, end_x, end_y)
        self.sleep(1)

    def swipe_left_default(self):
        logger.info("action: swipe left as default")

        height = self.window_info[1]
        weight = self.window_info[2]

        # 起点横坐标为屏幕左侧三分之一, 纵坐标为屏幕中点
        start_x = int(weight / 3)
        start_y = int(height * 0.5)

        # 终点横坐标为右侧三分之一, 纵坐标为屏幕中点(与起点纵坐标一致)
        end_x = int(weight * 2 / 3)
        end_y = start_x
        self.swipe(start_x, start_y, end_x, end_y)

    def swipe_right_default(self):
        logger.info("action: swipe right as default")

        height = self.window_info[1]
        weight = self.window_info[2]

        # 起点横坐标为屏幕右侧三分之一, 纵坐标为屏幕中点
        start_x = int(weight * 2 / 3)
        start_y = int(height * 0.5)

        # 终点横坐标为左侧三分之一, 纵坐标为屏幕中点(与起点纵坐标一致)
        end_x = int(weight / 3)
        end_y = start_x
        self.swipe(start_x, start_y, end_x, end_y)

    def find_element_without_exception(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
            logger.error("action : element found; xpath is {0}".format(xpath))
        except ElementFoundError:
            logger.error("info : xpath element {0} is not found".format(xpath))
            pass
        return element

    def find_element(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
            logger.info("action : element found; xpath is {0}".format(xpath))
        except ElementFoundError:
            raise("info : xpath element {0} is not found".format(xpath))
        return element

    def page_source(self):
        logger.info("action: get page source")
        ps = self.driver.page_source
        return ps

    def launch_app(self):
        """
        Start on the device the application specified in the desired capabilities
        """
        driver = self.driver.launch_app()
        logger.info("action: launch")
        self.driver = driver

    def activate_app(self, package_name):
        """
        Activates the application if it is not running
        or is running in the background
        """
        logger.info("action : activate app")
        driver = self.driver.activate_app(package_name)
        self.driver = driver

    def take_screenshot(self):
        pic_name = self.__screen_shot_name()
        self.driver.get_screenshot_as_file(pic_name)
        logger.info("action: create screen shot picture : {0}".format(pic_name))
        return pic_name

    def __screen_shot_name(self):
        return self.screen_shot_dir + os.path.sep + "{0}.png".format(TimeUtils.get_current_time_for_output())

    def draw_circle(self, bounds, pic_name):
        image_file = pic_name
        img = cv2.imread(image_file)
        center = bounds
        radius = 40
        color = (255, 0, 0)
        thickness = 4
        cv2.circle(img, center, radius, color, thickness)
        cv2.imwrite(image_file, img)
