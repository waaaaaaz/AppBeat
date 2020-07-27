# coding: utf-8

import json
from .base import Base
from log import Log
from setting import DFS_MAX_DEPTH

logger = Log.logger(__file__)


class DFSModel(Base):

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

    def init(self):
        self.common_init()

    def click(self, loop_count=DFS_MAX_DEPTH):
        if loop_count == 0:
            return
        logger.info("-" * 30 + "dfs loop count is {0}".format(loop_count) + "-" * 30 )
        self.update_action_count()
        self.driver.click_by_coordinate(self.focus_bounds)
        self.driver.sleep(1)
        self.update_app_status()
        self.update_exe_after_click()
        loop_count -= 1
        self.click(loop_count)
        logger.info("exe records is {0}".format(json.dumps(self.exe_records, ensure_ascii=False)))

    def update_exe_after_click(self):
        current_activity_key, clickable_item_dict, current_page_source, similar_known_activity_key = self.current_activity_status()
        if self.last_activity == current_activity_key and self.last_activity != self.root_activity:
            self.exe()
        similar_known_activity_key = self.similar_known_activity_key_in_records(current_activity_key)
        if similar_known_activity_key is None:
            self.add_new_activity_to_records(current_activity_key, clickable_item_dict)
            self.update_bounds()
        else:
            self.known_activity_todo(similar_known_activity_key)