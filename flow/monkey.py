# coding: utf-8

import random

from .base import Base
from log import Log


logger = Log.logger(__file__)


class MONKEYModel(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.monkey_percentage = self.rule.MONKEY_PERCENTAGE
        self.init()

    def init(self):
        self.driver.sleep(5)
        self.init_steps()

    def exe(self):
        logger.info("-" * 30 + " step 1 " + "-" * 30)
        self.next_action()
        logger.info("-" * 30 + " step 2 " + "-" * 30)
        self.update_app_status()
        logger.info("steps are {0}".format(self.steps))

    def next_action(self):
        action = self.dict_ratio_random()
        action_name = action.replace("PER", "monkey").lower()
        logger.info("current monkey action is {0}".format(action_name))
        func = getattr(self, action_name)
        self.update_action_count()
        func()

    def dict_ratio_random(self):
        item_list = []
        for k, v in self.monkey_percentage.items():
            item_list = item_list + [k] * v
        return random.choice(item_list)

    def monkey_click(self):
        current_activity_key, clickable_item_dict, current_page_source = self.get_page_structure()
        if clickable_item_dict is None:
            return
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        bounds_key = random.choice(list(clickable_item_dict))
        bounds = clickable_item_dict[bounds_key]["bounds"]
        steps = "{0} ||| {1} ||| {2}".format(current_activity_key, "click", bounds)
        self.steps.append(steps)
        self.driver.click_by_coordinate(bounds)

    def monkey_double_click(self):
        current_activity_key, clickable_item_dict, current_page_source = self.get_page_structure()
        if clickable_item_dict is None:
            return
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        bounds_key = random.choice(list(clickable_item_dict))
        bounds = clickable_item_dict[bounds_key]["bounds"]
        steps = "{0} ||| {1} ||| {2}".format(current_activity_key, "double_click", bounds)
        self.steps.append(steps)
        self.driver.double_click_by_coordinate(bounds)

    def monkey_swipe_up(self):
        current_activity_key = self.get_page_structure()[0]
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        steps = "{0} ||| {1}".format(current_activity_key, "swipe_up")
        self.steps.append(steps)
        self.driver.swipe_up_default()

    def monkey_swipe_down(self):
        current_activity_key = self.get_page_structure()[0]
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        steps = "{0} ||| {1}".format(current_activity_key, "swipe_down")
        self.steps.append(steps)
        self.driver.swipe_down_default()

    def monkey_long_press(self):
        current_activity_key, clickable_item_dict, current_page_source = self.get_page_structure()
        if clickable_item_dict is None:
            return
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        bounds_key = random.choice(list(clickable_item_dict))
        bounds = clickable_item_dict[bounds_key]["bounds"]
        steps = "{0} ||| {1} ||| {2}".format(current_activity_key, "long_press", bounds)
        self.steps.append(steps)
        self.driver.long_press_by_coordinate(bounds)

    def monkey_pinch(self):
        current_activity_key = self.get_page_structure()[0]
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        steps = "{0} ||| {1}".format(current_activity_key, "pinch")
        self.steps.append(steps)
        self.driver.default_pinch()

    def monkey_unpinch(self):
        current_activity_key = self.get_page_structure()[0]
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        steps = "{0} ||| {1}".format(current_activity_key, "unpinch")
        self.steps.append(steps)
        self.driver.default_unpinch()

    def monkey_drag(self):
        current_activity_key = self.get_page_structure()[0]
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        steps = "{0} ||| {1}".format(current_activity_key, "drag")
        self.steps.append(steps)
        self.driver.drag()

    def monkey_back_key(self):
        current_activity_key = self.get_page_structure()[0]
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        steps = "{0} ||| {1}".format(current_activity_key, "back_key")
        self.steps.append(steps)
        self.driver.press_back()

    def monkey_home_key(self):
        current_activity_key = self.get_page_structure()[0]
        if len(self.steps) >= 5 and self.update_page_status(current_activity_key) is False:
            self.driver.launch_app()
        steps = "{0} ||| {1}".format(current_activity_key, "home_key")
        self.steps.append(steps)
        self.driver.press_home()

    def monkey_launch(self):
        steps = "launch"
        self.steps.append(steps)
        self.driver.launch_app()

    def monkey_activate(self):
        steps = "activate"
        self.steps.append(steps)
        self.driver.activate_app()

    def update_app_status(self):
        logger.info("action : app status update")
        status = self.driver.get_app_status()
        if status in [0, 1]:
            if self.driver.is_process_exist() is False:
                logger.info("status : app crashed")
            else:
                logger.info("status : app dead")
            self.monkey_launch()
            self.update_app_status()
        elif status in [2, 3]:
            logger.info("status : app in background")
            self.monkey_activate()
            self.update_app_status()
        logger.info("status : app works well")

    def update_page_status(self, current_activity_key):
        # 最近的5个页面
        last_activity_keys = self.steps[:-6:-1]
        same_count = 0
        for i in last_activity_keys:
            if self.is_same_activity_key(i.split(" ||| ")[0], current_activity_key):
                same_count += 1
        if same_count == 5:
            return False
        return True
