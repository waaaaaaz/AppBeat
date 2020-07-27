# coding: utf-8

import json

from .base import Base
from log import Log
from setting import RecordsStatus, MAX_SWIPE_DOWN_COUNT
from exception import ValidationError

logger = Log.logger(__file__)


class TARGETModel(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.target_list = []
        self.init()

    def exe(self):
        logger.info("-" * 30 + " step 1 " + "-" * 30)
        self.go_to_target()
        logger.info("-" * 30 + " step 2 " + "-" * 30)
        self.update_exe_on_target()
        logger.info("-" * 30 + " step 3 " + "-" * 30)
        self.click()
        logger.info("-" * 30 + " step 4 " + "-" * 30)
        self.update_app_status()

    def init(self):
        for i in self.rule.TARGET_SETTING:
            steps = i["STEPS"]
            if steps[0] != "LAUNCH":
                steps = ["LAUNCH"] + steps
            exe_key = " ||| ".join(steps)
            if exe_key not in self.target_list:
                self.target_list.append(exe_key)
                self.exe_records[exe_key] = {}
                self.exe_records[exe_key]["0"] = {}
                self.exe_records[exe_key]["status"] = RecordsStatus.TO_DO
                self.exe_records[exe_key]["roll_back_steps"] = steps
                if "TARGET_ACTIVITY" in i.keys():
                    self.exe_records[exe_key]["target_activity"] = i["TARGET_ACTIVITY"]
                if "TARGET_TEXT" in i.keys():
                    self.exe_records[exe_key]["target_text"] = i["TARGET_TEXT"]

        self.driver.sleep(5)
        self.target_activity = self.target_list[0]

        current_activity_key, clickable_item_dict, current_page_source = self.get_page_structure()
        self.root_activity = current_activity_key

        if self.target_activity == "LAUNCH":
            self.exe_records[exe_key]["0"] = clickable_item_dict

        logger.info(json.dumps(self.exe_records, ensure_ascii=False))

    def go_to_target(self):
        logger.info("action : go to target page")

        status = self.update_activity_status(self.target_activity)
        logger.info("go_to_target ::: target activity status is {0}".format(status))
        if status == RecordsStatus.DONE:
            logger.info("should switch target activity, exe records is {0}".format(
                json.dumps(self.exe_records, ensure_ascii=False)))
            self.update_target()
            self.exe()

        self.current_activity_status()

        if self.current_activity == self.target_activity:
            logger.info("当前页面是target页面, target activity key is {0}".format(self.target_activity))
            return
        else:
            logger.info("当前页面不是target页面")

        if self.current_activity != self.root_activity:
            self.back_to_root()

        # current page is root

        if self.target_activity == self.root_activity:
            self.known_activity_todo(self.root_activity)
        else:
            self.go_to_target_by_steps()  # click to target page

    def go_to_target_by_steps(self):
        for step in self.exe_records[self.target_activity]["roll_back_steps"][1:]:
            tmp = step.split(" ||| ")
            action = tmp[0]
            xpath = tmp[1]
            element = self.driver.find_element(xpath)
            if action == "CLICK":
                self.driver.click_element(element)
                self.driver.sleep()
            if action == "ENTER":
                text = tmp[2]
                element.send_keys(text)
                self.driver.sleep()

            if "target_activity" in self.exe_records[self.target_activity].keys():
                if self.validate_target_activity(self.exe_records[self.target_activity]["target_activity"]) is False:
                    raise ValidationError("different target activity in config file")
            if "target_text" in self.exe_records[self.target_activity].keys():
                if self.validate_target_text(self.exe_records[self.target_activity]["target_text"]) is False:
                    raise ValidationError("different target activity in config file")
        self.current_activity = self.target_activity

    def validate_target_activity(self, target_activity):
        current_android_activity = self.driver.current_activity()
        if current_android_activity == target_activity:
            return True
        return False

    def validate_target_text(self, target_text: list):
        current_activity_key = self.get_page_structure()[0]
        current_activity_key_list = current_activity_key.split(" |||| ")
        for i in target_text:
            if i not in current_activity_key_list:
                return False
        return True

    def update_exe_on_target(self):
        status = self.update_activity_status(self.target_activity)
        if status == RecordsStatus.TO_SWIPE:
            activity_swipe_count = self.latest_swipe_count(self.target_activity)
            self.bounds_swipe_count = activity_swipe_count + 1
            for i in range(0, self.bounds_swipe_count):
                self.swipe_up()
            if self.target_activity == self.root_activity:
                action = "launch ||| {0}".format(self.bounds_swipe_count)
                self.steps = [action]
            else:
                action = "click ||| {0} ||| {1}".format(self.bounds_swipe_count, self.focus_bounds)
                self.steps = self.steps.append(action)
            current_activity_key, clickable_item_dict, current_page_source = self.get_page_structure()
            self.update_known_activity_records(current_page_source, self.target_activity,
                                               self.bounds_swipe_count)

        if status == RecordsStatus.TO_DO:
            self.update_bounds()
        if status == RecordsStatus.DONE:
            self.exe()

    def click(self):
        self.update_action_count()
        self.driver.click_by_coordinate(self.focus_bounds)
        self.driver.sleep(1)

    def update_activity_status(self, activity_key=None):
        if activity_key is None:
            activity_key = self.current_activity

        if self.exe_records[activity_key]["status"] == RecordsStatus.DONE:
            return self.exe_records[activity_key]["status"]

        activity_swipe_count = self.latest_swipe_count(activity_key)

        if activity_swipe_count is None:
            self.exe_records[activity_key]["status"] = RecordsStatus.DONE
            return self.exe_records[activity_key]["status"]

        for k in self.exe_records[activity_key].keys():
            if k not in ["roll_back_steps", "status", "target_activity", "target_text"]:
                for kk, vv in self.exe_records[activity_key][k].items():
                    if vv["covered"] is False:
                        self.exe_records[activity_key]["status"] = RecordsStatus.TO_DO
                        return self.exe_records[activity_key]["status"]

        if activity_swipe_count < MAX_SWIPE_DOWN_COUNT:
            self.exe_records[activity_key]["status"] = RecordsStatus.TO_SWIPE
        else:
            self.exe_records[activity_key]["status"] = RecordsStatus.DONE

        return self.exe_records[activity_key]["status"]

    def current_activity_status(self):
        current_activity_key, clickable_item_dict, current_page_source = self.get_page_structure()
        if self.is_root_page(current_activity_key):
            self.init_steps()
            similar_known_activity_key = self.root_activity
            self.update_current_activity(self.root_activity)
            return current_activity_key, clickable_item_dict, current_page_source, similar_known_activity_key

        similar_known_activity_key = self.similar_known_activity_key_in_records(current_activity_key)
        if similar_known_activity_key is None:
            self.update_current_activity(current_activity_key)
        else:
            self.update_current_activity(similar_known_activity_key)
        return current_activity_key, clickable_item_dict, current_page_source, similar_known_activity_key

    def is_root_page(self, current_activity_key):
        logger.info("action : confirm it is root page or not")
        if self.is_same_activity_key(self.root_activity, current_activity_key):
            logger.info("info : current page is root page")
            return True
        else:
            logger.info("info : current page is not root page")
            return False

    def back_to_root(self, back_loop_count=3):
        """
        返回初始页面
        判断: 获取activity = root activity, page_source = root page source
        :return:
        """
        logger.info("action: back to root page")
        # 多次返回回不到初始页面, 重新启动
        if back_loop_count <= 0:
            logger.info("info : cannot turn back to root, try 3 times")
            self.launch()
            return
            # self.init_steps()
        logger.info("action : press back count is {0}".format(str(back_loop_count)))
        self.back()
        current_activity_key = self.get_page_structure()[0]
        if self.is_root_page(current_activity_key) is False:
            back_loop_count -= 1
            self.back_to_root(back_loop_count)
        else:
            self.init_steps()
            self.update_current_activity(self.root_activity)
            logger.info("info : back to root successfully")