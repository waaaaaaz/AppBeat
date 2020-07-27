# coding: utf-8

from appium import webdriver
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction

from .base import Base
from log import Log
from utils import CommandUtils
from exception import CommandError, UDIDError

logger = Log.logger(__file__)


class ANDROIDDriver(Base):

    def __init__(self, rule):
        super().__init__(rule)
        self.rule = rule
        self.package_name = self.rule.ANDROID_PACKAGE_REQUIRED
        self.main_activity = self.rule.ANDROID_MAIN_ACTIVITY_REQUIRED
        self.driver = self.driver()
        self.app_name = self.package_name
        self.process_name = self.app_name.lower()
        self.window_info = self.window_info()

    def android_driver_prepare(self):
        logger.info("info : android app package startup ::: {0}".format(self.package_name))
        url, caps = self.common_driver_prepare()
        caps["platformName"] = "Android"
        caps["appPackage"] = self.package_name
        caps["appActivity"] = self.main_activity
        caps["resetKeyboard"] = True
        caps["unicodeKeyboard"] = True

        if int(self.android_sdk_version(self.udid)) > 23:  # Android 7要用 uiautomator2
            caps["automationName"] = "uiautomator2"
            logger.info("info : uiautomator2 referred by appium")

        return url, caps

    def driver(self):
        url, caps = self.android_driver_prepare()
        driver = webdriver.Remote(url, caps)
        return driver

    def is_process_exist(self):
        # adb命令查找进程名字, 找不到说明crash
        logger.info("action : confirm app process exist or not")
        process_exist = True
        cmd = CommandUtils.is_android_process_exist(self.rule.udid, self.process_name)
        stdout, stderr = CommandUtils.command_exe(cmd)
        if len(stdout) == 0:
            logger.info("info : Android Package: {0} not found in process list.It is crashed.".format(
                self.process_name))
            process_exist = False
        else:
            if self.process_name not in stdout[0]:
                logger.info("info : Android Package: {0} not found in process list.It is crashed.".format(
                    self.process_name))
                process_exist = False
        return process_exist

    def press_back(self):
        logger.info("action : press back")
        try:
            self.press_key_code(AndroidKey.BACK)
        except:
            pass

    def activate_app(self):
        """
        Activates the application if it is not running
        or is running in the background
        """
        logger.info("action : activate app")
        driver = self.driver.activate_app(self.package_name)
        self.driver = driver

    def press_home(self):
        # logger.info("appium action : press home")
        self.driver.press_keycode(AndroidKey.HOME)

    def press_key_code(self, android_key_code):
        self.driver.press_keycode(android_key_code)

    def current_activity(self):
        activity = self.driver.current_activity
        logger.info("info : current activity is : {0}".format(activity))
        return activity

    def android_sdk_version(self, udid):
        cmd = CommandUtils.android_sdk_version(udid)
        stdout, stderr = CommandUtils.command_exe(cmd)
        if len(stderr) == 1:
            raise UDIDError("Fail to get sdk version; udid : {0} is wrong!".format(udid))
        elif len(stdout) != 1:
            raise CommandError("cmd result is wrong; cmd ==> {0}".format(cmd.join(" ")))
        logger.info("info : current android sdk version is {0}".format(stdout[0]))
        return stdout[0]

    def drag(self):

        window_info = self.window_info
        height = window_info[1]
        weight = window_info[2]

        # 起点横坐标为屏幕中点, 纵坐标为屏幕上方三分之一
        start_x = int(weight * 0.5)
        start_y = int(height / 3)

        # 终点横坐标为屏幕中点(与起点横坐标一致), 纵坐标为屏幕下方三分之一
        end_x = start_x
        end_y = int(height * 2 / 3)

        action = TouchAction(self.driver)

        # if self.rule.is_android():
        action.long_press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).release().perform()

    def default_pinch(self):

        window_info = self.window_info
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
        action_head.press(x=head_x, y=head_y).move_to(x=line_center_x, y=line_center_y).release()
        action_tail.press(x=tail_x, y=tail_y).move_to(x=line_center_x, y=line_center_y).release()

        multi_action = MultiAction(self.driver)
        multi_action.add(action_head)
        multi_action.add(action_tail)
        multi_action.perform()

    def default_unpinch(self):
        window_info = self.window_info
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
        action_head.press(x=line_center_x, y=line_center_y).move_to(x=head_x, y=head_y).release()
        action_tail.press(x=line_center_x, y=line_center_y).move_to(x=tail_x, y=tail_y).release()

        multi_action = MultiAction(self.driver)
        multi_action.add(action_head)
        multi_action.add(action_tail)
        multi_action.perform()

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
        status = self.driver.query_app_state(self.package_name)
        logger.info("info : app status code is {0}".format(str(status)))
        return status
