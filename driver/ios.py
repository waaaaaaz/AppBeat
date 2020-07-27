# coding: utf-8

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction

from .base import Base
from log import Log
from utils import CommandUtils
from setting import APPIUM_IOS_WDA_PORT

logger = Log.logger(__file__)


class IOSDriver(Base):

    def __init__(self, rule):
        super().__init__(rule)
        self.rule = rule
        self.bundle_id = self.rule.IOS_BUNDLE_ID_REQUIRED.lower()
        self.app_name = self.rule.IOS_BUNDLE_NAME_REQUIRED.lower()
        self.process_name = self.rule.IOS_IPA_NAME_REQUIRED.lower()
        self.appium_wda_port = APPIUM_IOS_WDA_PORT
        self.driver = self.driver()
        self.window_info = self.window_info()

    def __ios_driver_prepare(self):
        logger.info("iso app package startup ::: {0}".format(self.bundle_id))

        url, caps = self.common_driver_prepare()

        caps["platformName"] = "iOS"
        caps["automationName"] = "XCUITest"
        caps["bundleId"] = self.bundle_id
        caps["udid"] = self.rule.udid
        caps["wdaConnectionTimeout"] = 1800 * 1000
        caps["wdaLocalPort"] = self.appium_wda_port
        caps["startIWDP"] = True
        caps["autoAcceptAlerts"] = True

        return url, caps

    def driver(self):
        url, caps = self.__ios_driver_prepare()
        driver = webdriver.Remote(url, caps)
        return driver

    def is_process_exist(self):
        # Crash report中找到了ipa的名字，说明crash了
        process_exist = True
        cmd = CommandUtils.is_ios_process_exist(self.rule.udid)
        stdout, stderr = CommandUtils.command_exe(cmd)
        if self.process_name in stdout:
            logger.info("========!!!!!!!!!!!iOS IPA: {0} crashed!!!!".format(self.process_name))
            process_exist = False
        return process_exist

    def press_back(self):
        logger.info("action : press back")
        self.swipe_right_default()

    def get_app_status(self):
        """
        :return:
        0: The current application state cannot be determined/is unknown
        1: The application is not running
        2: The application is running in the background and is suspended
        3: The application is running in the background and is not suspended
        4: The application is running in the foreground
        """
        logger.info("action : get app status")
        status = self.driver.query_app_state(self.bundle_id)
        logger.info("info : app status code is {0}".format(str(status)))
        return status
        # return self.driver.query_app_state(self.bundle_id)

    def activate_app(self):
        """
        Activates the application if it is not running
        or is running in the background
        """
        driver = self.driver.activate_app(self.bundle_id)
        self.driver = driver

    def drag(self):
        window_info = self.window_info()
        height = window_info[1]
        weight = window_info[2]

        # 起点横坐标为屏幕中点, 纵坐标为屏幕上方三分之一
        start_x = int(weight * 0.5)
        start_y = int(height / 3)

        # 终点横坐标为屏幕中点(与起点横坐标一致), 纵坐标为屏幕下方三分之一
        end_x = start_x
        end_y = int(height * 2 / 3)

        action = TouchAction(self.driver)
        action.long_press(x=start_x, y=start_y, duration=2000).move_to(x=end_x, y=end_y).release().perform()

    def default_pinch(self):
        window_info = self.window_info()
        height = window_info[1]
        weight = window_info[2]

        # 起点横坐标为屏幕中点, 纵坐标为屏幕中点
        head_x = int(weight * 0.5)
        head_y = int(height * 0.5)

        # 终点横坐标为屏幕中点(与起点横坐标一致), 纵坐标为屏幕下方三分之一
        tail_x = head_x + 400
        tail_y = head_y

        line_center_x = (head_x + tail_x) / 2
        line_center_y = (head_y + tail_y) / 2

        action_head = TouchAction(self.driver)
        action_tail = TouchAction(self.driver)

        # 缩小pinch
        action_head.long_press(x=head_x, y=head_y, duration=200).move_to(x=line_center_x - head_x,
                                                                         y=0).release()
        action_tail.long_press(x=tail_x, y=tail_y, duration=200).move_to(x=line_center_x - tail_x,
                                                                         y=0).release()

        multi_action = MultiAction(self.driver)
        multi_action.add(action_head)
        multi_action.add(action_tail)
        multi_action.perform()

    def default_unpinch(self):
        window_info = self.window_info()
        height = window_info[1]
        weight = window_info[2]

        # 起点横坐标为屏幕中点, 纵坐标为屏幕中点
        head_x = int(weight * 0.5)
        head_y = int(height * 0.5)

        # 终点横坐标为屏幕中点(与起点横坐标一致), 纵坐标为屏幕下方三分之一
        tail_x = head_x + 400
        tail_y = head_y

        line_center_x = (head_x + tail_x) / 2
        line_center_y = (head_y + tail_y) / 2

        action_head = TouchAction(self.driver)
        action_tail = TouchAction(self.driver)

        # 放大 unpinch
        action_head.long_press(x=line_center_x, y=line_center_y, duration=200).move_to(x=100, y=0).release()
        action_tail.long_press(x=line_center_x, y=line_center_y, duration=200).move_to(x=-100, y=0).release()

        multi_action = MultiAction(self.driver)
        multi_action.add(action_head)
        multi_action.add(action_tail)
        multi_action.perform()
