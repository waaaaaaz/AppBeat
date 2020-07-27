# coding: utf-8

import json

from .base import Base
from log import Log

logger = Log.logger(__file__)


class BFSModel(Base):

    def __init__(self, driver):
        super().__init__(driver)
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
        logger.info("-" * 30 + " step 5 " + "-" * 30)
        self.update_exe_after_click()

    def init(self):
        self.common_init()

    def update_exe_after_click(self):
        current_activity_key, clickable_item_dict, current_page_source, similar_known_activity_key = self.current_activity_status()
        if self.last_activity == current_activity_key and self.last_activity != self.root_activity:
            self.exe()
        similar_known_activity_key = self.similar_known_activity_key_in_records(current_activity_key)
        if similar_known_activity_key is None:
            self.add_new_activity_to_records(current_activity_key, clickable_item_dict)

    def click(self):
        self.update_action_count()
        self.driver.click_by_coordinate(self.focus_bounds)
        self.driver.sleep(1)
