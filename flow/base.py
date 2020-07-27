# coding: utf-8

from abc import abstractmethod, ABCMeta
import json
from copy import deepcopy

from setting import MAX_SWIPE_DOWN_COUNT, RecordsStatus
from log import Log
from utils import XPathUtils, TimeUtils

logger = Log.logger(__file__)


class Base(object):
    __metaclass__ = ABCMeta

    action_mappoing = {
        "launch": "launch",
        "activate": "activate",
        "click": "click",
        "turn_back": "turn_back",
        "swipe_down": "swipe_down"
    }

    @abstractmethod
    def __init__(self, driver):
        self.driver = driver
        self.rule = driver.rule
        self.mode = self.rule.mode
        self.steps = []
        self.page_list = []
        self.exe_records = {}
        self.action_count = 0
        self.root_activity = None
        self.app_name = self.driver.app_name
        self.process_name = self.driver.process_name
        self.focus_bounds = None
        self.target_activity = None
        self.bounds_swipe_count = 0
        self.last_activity = None
        self.current_activity = None
        self.full_path = None

    @abstractmethod
    def exe(self):
        raise NotImplementedError

    def back(self):
        self.driver.press_back()

    def launch(self):
        self.driver.launch_app()
        self.driver.sleep(5)
        self.init_steps()
        self.update_current_activity(self.root_activity)

    def activate(self):
        self.driver.activate_app()
        self.driver.sleep(1)
        self.init_steps()
        self.update_current_activity(self.root_activity)

    def swipe_up(self):
        self.driver.swipe_up_default()

    def update_steps(self):
        action = "click ||| {0} ||| {1}".format(self.bounds_swipe_count, self.focus_bounds)
        self.steps.append(action)

    def common_init(self):
        self.driver.sleep(5)
        current_activity_key, clickable_item_dict, current_page_source = self.get_page_structure()
        self.root_activity = current_activity_key
        self.target_activity = current_activity_key
        self.current_activity = current_activity_key
        self.page_list.append(self.target_activity)
        self.exe_records[self.target_activity] = {}
        self.exe_records[self.target_activity]["0"] = clickable_item_dict
        self.exe_records[self.target_activity]["status"] = RecordsStatus.TO_DO
        self.exe_records[self.target_activity]["roll_back_steps"] = ["launch"]
        self.init_steps()
        logger.info("info : exe records init: {0}".format(json.dumps(self.exe_records, ensure_ascii=False)))

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
        if self.is_root_page() is False:
            back_loop_count -= 1
            self.back_to_root(back_loop_count)
        else:
            self.init_steps()
            self.update_current_activity(self.root_activity)
            logger.info("info : back to root successfully")

    def is_root_page(self, current_activity_key=None):
        logger.info("action : confirm it is root page or not")
        if current_activity_key is None:
            current_activity_key = self.get_page_structure()[0]
            self.update_current_activity(current_activity_key)
        if self.is_same_activity_key(self.root_activity, self.current_activity):
            logger.info("info : current page is root page")
            return True
        else:
            logger.info("info : current page is not root page")
            return False

    def is_same_activity_key(self, known_key, new_key):
        known_key_list = known_key.split(" |||| ")
        new_key_list = new_key.split(" |||| ")
        benchmark = int(len(known_key_list) * 0.7)
        if benchmark == 0:
            logger.info("info : diff activity : benchmark is {0}".format(benchmark))
            return False
        known_count = 0
        for i in known_key_list:
            if i in new_key_list:
                known_count += 1
        new_count = 0
        for i in new_key_list:
            if i in known_key_list:
                new_count += 1
        if known_count <= new_count:
            same_count = known_count
        else:
            same_count = new_count
        if same_count >= benchmark:
            logger.info("info : same activity : same count is {0}; benchmark is {1}".format(same_count, benchmark))
            return True
        else:
            logger.info("info : diff activity : same count is {0}; benchmark is {1}".format(same_count, benchmark))
            return False

    def get_activity_key_and_clickable_dict(self, current_page_source):
        clickable_item_dict = XPathUtils.page_clickable_item_update(current_page_source)
        clickable_item_dict_back = self.build_clickable_item_dict_back(clickable_item_dict)
        page_text_list = XPathUtils.page_text_list(current_page_source)
        current_activity_key = self.build_activity_key(page_text_list)
        return current_activity_key, clickable_item_dict_back

    def build_clickable_item_dict_back(self, clickable_item_dict):
        count = 3
        clickable_item_dict_back = {}
        for k, v in clickable_item_dict.items():
            if count > 0:
                clickable_item_dict_back[k] = v
                count -= 1
            else:
                return clickable_item_dict_back

    def get_page_structure(self, loop_count=150):
        if loop_count == 0:
            self.exe()
        current_page_source = self.driver.page_source()
        if current_page_source == "" or current_page_source is None:
            loop_count -= 1
            self.get_page_structure(loop_count)
        current_activity_key, clickable_item_dict = self.get_activity_key_and_clickable_dict(current_page_source)
        if current_activity_key == "" or current_page_source is None:
            loop_count -= 1
            self.get_page_structure(loop_count)
        return current_activity_key, clickable_item_dict, current_page_source

    def build_activity_key(self, text_list):
        activity_key = ""
        for k in text_list:
            if activity_key == "":
                activity_key = k
            else:
                activity_key = activity_key + " |||| {0}".format(k)
        return activity_key

    def go_to_target(self):
        logger.info("action : go to target page")

        status = self.update_activity_status(self.target_activity)
        logger.info("go_to_target ::: target activity status is {0}".format(status))
        if status == RecordsStatus.DONE:
            logger.info("should switch target activity, exe records is {0}".format(json.dumps(self.exe_records, ensure_ascii=False)))
            self.update_target()
            self.exe()

        self.current_activity_status()

        if self.is_same_activity_key(self.target_activity, self.current_activity) is True:
            logger.info("当前页面是target页面, target activity key is {0}".format(self.target_activity))
            return
        else:
            logger.info("当前页面不是target页面")

        if self.is_root_page(self.current_activity) is False:
            self.back_to_root()

        # current page is root

        if self.target_activity == self.root_activity:
            self.known_activity_todo(self.root_activity)
        else:
            self.click_to_target()  # click to target page

    def click_to_target(self):
        logger.info("click to target")
        logger.info("roll back steps is {0}".format(self.exe_records[self.target_activity]["roll_back_steps"]))
        click_steps = deepcopy(self.exe_records[self.target_activity]["roll_back_steps"][1:])
        root_step = deepcopy(self.exe_records[self.target_activity]["roll_back_steps"][0])
        logger.info(root_step)
        if "|||" in root_step:
            swipe_count = int(root_step.split(" ||| ")[1])
            for _ in range(0, swipe_count):
                self.swipe_up()

        logger.info("should click to target page")
        logger.info("click steps is {0}".format(click_steps))
        for i in click_steps:
            swipe_count = int(i.split(" ||| ")[1])
            position = (
                int(i.split(" ||| ")[2].split(", ")[0].lstrip("(")),
                int(i.split(" ||| ")[2].split(", ")[1].rstrip(")")))
            logger.info("click to target, position is {0}".format(position))
            for _ in range(0, swipe_count):
                self.swipe_up()
            self.driver.click_by_coordinate(position)
            self.driver.sleep(1)
        self.steps = self.exe_records[self.target_activity]["roll_back_steps"]
        logger.info("已经通过回溯步骤到达target页面")

    def update_target(self):
        self.target_activity = self.page_list[self.page_list.index(self.target_activity) + 1]
        status = self.update_activity_status(self.target_activity)
        if status == RecordsStatus.DONE:
            self.update_target()

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

    def update_exe_on_target(self):
        current_activity_key, clickable_item_dict, current_page_source, similar_known_activity_key = self.current_activity_status()
        similar_known_activity_key = self.similar_known_activity_key_in_records(current_activity_key)
        if similar_known_activity_key is None:
            self.add_new_activity_to_records(current_activity_key, clickable_item_dict)
        else:
            self.known_activity_todo(similar_known_activity_key)

    def update_current_activity(self, current_activity_key):
        self.last_activity = self.current_activity
        self.current_activity = current_activity_key

    def known_activity_todo(self, similar_known_activity_key):
        if self.current_activity != similar_known_activity_key:
            self.update_current_activity(similar_known_activity_key)
        status = self.update_activity_status(self.current_activity)
        if status == RecordsStatus.TO_SWIPE:
            activity_swipe_count = self.latest_swipe_count(similar_known_activity_key)
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
            self.update_known_activity_records(current_page_source, similar_known_activity_key,
                                               self.bounds_swipe_count)

        if status == RecordsStatus.TO_DO:
            self.update_bounds()
        if status == RecordsStatus.DONE:
            self.exe()

    def update_exe_after_target(self, similar_known_activity_key, swipe_count):
        current_activity_key, clickable_item_dict, current_page_source = self.get_page_structure()
        status = self.update_known_activity_records(current_page_source, similar_known_activity_key,
                                                    swipe_count)
        if status == RecordsStatus.TO_DO:
            self.update_bounds()
        else:
            self.exe()

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
            if k not in ["roll_back_steps", "status"]:
                for kk, vv in self.exe_records[activity_key][k].items():
                    if vv["covered"] is False:
                        self.exe_records[activity_key]["status"] = RecordsStatus.TO_DO
                        return self.exe_records[activity_key]["status"]

        if activity_swipe_count < MAX_SWIPE_DOWN_COUNT:
            self.exe_records[activity_key]["status"] = RecordsStatus.TO_SWIPE
        else:
            self.exe_records[activity_key]["status"] = RecordsStatus.DONE

        return self.exe_records[activity_key]["status"]

    def update_action_count(self):
        self.action_count += 1

    def update_bounds(self, ):
        result = self.get_bounds()
        if result is False:
            self.exe()

    def get_bounds(self):
        activity_key = self.current_activity
        for k in self.exe_records[activity_key].keys():
            if k not in ["roll_back_steps", "status"]:
                for kk, vv in self.exe_records[activity_key][k].items():
                    if vv["covered"] is False:
                        bounds = vv["bounds"]
                        self.focus_bounds = bounds
                        self.full_path = kk
                        self.exe_records[activity_key][k][kk][
                            "covered"] = True
                        timestamp = TimeUtils.get_current_timestamp()
                        self.exe_records[activity_key][k][kk][
                            "timestamp"] = timestamp
                        logger.info("exe records is {0}".format(json.dumps(self.exe_records, ensure_ascii=False)))
                        logger.info("info : current focus bounds : {0}".format(self.focus_bounds))
                        return True
        self.exe_records[activity_key]["status"] = RecordsStatus.DONE
        return False

    def add_new_activity_to_records(self, activity_key, clickable_item_dict):
        if activity_key is None or activity_key == "" or clickable_item_dict is None:
            self.exe()
        else:
            self.exe_records[activity_key] = {}
            self.update_steps()
            self.exe_records[activity_key]["roll_back_steps"] = self.steps
            self.exe_records[activity_key]["0"] = clickable_item_dict
            self.exe_records[activity_key]["status"] = RecordsStatus.TO_DO
            self.page_list.append(activity_key)
            self.update_current_activity(activity_key)

    def update_known_activity_records(self, current_page_source, activity_key, swipe_count):
        logger.info("known activity key is : {0}".format(activity_key))
        logger.info("tag exe records is {0}".format(json.dumps(self.exe_records, ensure_ascii=False)))
        clicked_list = []
        for count in range(0, swipe_count):
            for k in self.exe_records[activity_key][str(count)].keys():
                if k not in clicked_list:
                    clicked_list.append(k)
        clickable_item_dict = XPathUtils.page_clickable_item_update(current_page_source, clicked_list)

        if len(clickable_item_dict) > 0:
            clickable_item_dict_back = self.build_clickable_item_dict_back(clickable_item_dict)
            self.exe_records[activity_key][str(swipe_count)] = clickable_item_dict_back
            self.exe_records[activity_key]["status"] = RecordsStatus.TO_DO
        else:
            self.exe_records[activity_key]["status"] = RecordsStatus.DONE
        return self.exe_records[activity_key]["status"]

    def similar_known_activity_key_in_records(self, activity_key):
        if len(self.exe_records) == 0:
            return None
        for known_activity_key in self.exe_records.keys():
            if self.is_same_activity_key(known_activity_key, activity_key):
                return known_activity_key
        return None

    def latest_swipe_count(self, activity_key):
        if activity_key in self.exe_records.keys():
            number_list = []
            for k in self.exe_records[activity_key].keys():
                if k not in ["roll_back_steps", "status", "target_activity", "target_text"]:
                    number_list.append(int(k))
            if len(number_list) > 0:
                return sorted(number_list)[-1]
        return None

    def update_app_status(self):
        logger.info("action : app status update")
        status = self.driver.get_app_status()
        if status in [0, 1]:
            if self.driver.is_process_exist() is False:
                logger.info("status : app crashed")
                self.exe_records[self.last_activity][self.bounds_swipe_count][self.full_path]["crashed"] = True
            else:
                logger.info("status : app dead")
            self.exe_records[self.last_activity][self.bounds_swipe_count][self.full_path]["crashed"] = False
            self.launch()
            self.exe()
        elif status in [2, 3]:
            logger.info("status : app in background")
            # self.activate()
            self.launch()
            self.exe()
        logger.info("status : app works well")

    def init_steps(self):
        # logger.info("重置回溯步骤")
        self.steps = ["launch"]

