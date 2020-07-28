# coding: utf-8

""" global setting for whole project """

import os


PROJECT_PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))


class RecordsStatus:
    TO_DO = "todo"
    TO_SWIPE = "to_swipe"
    DONE = "done"


# android app name xpath expr
ANDROID_APP_NAME_XPATH_EXPR = "(//*[@package!=''])[1]"
# ios app name xpath expr
IOS_APP_NAME_XPATH_EXPR = "//*[contains(@type,\"Application\")]"

# android clickable item xpath expr
ANDROID_CLICKABLE_XPATH_EXPR = "//*[@clickable='true']"

# ios clickable item xpath expr
IOS_CLICKABLE_XPATH_EXPR = '//*[@type="XCUIElementTypeCell" and @enabled="true"]'

# ios button item xpath expr
IOS_BUTTON_XPATH_EXPR = '//*[@type="XCUIElementTypeButton" and @enabled="true"]'




# all item xpath expr
ALL_XPATH_EXPR = "//*"

# android unclickable node tag
ANDROID_UNCLICKABLE_NODE_TAG = [
    "android.view.ViewGroup",
    "android.widget.FrameLayout",
    "android.widget.LinearLayout"
]

# execution mode
EXECUTION_MODE = [
    "bfs",
    "dfs",
    "monkey",
    "target"]

# required android config field

REQUIRED_ANDROID_CONFIG_FIELD = [
    "ANDROID_PACKAGE",
    "ANDROID_MAIN_ACTIVITY"
]

TARGET_CONFIG_FIELD = [
    "STEPS",
    "TARGET_TEXT",
    "TARGET_ACTIVITY"
]
# required ios config field

REQUIRED_IOS_CONFIG_FIELD = [
    "IOS_BUNDLE_ID",
    "IOS_BUNDLE_NAME",
    "IOS_IPA_NAME"
]

OPTIONAL_CONFIG_FIELD = {
    "MAX_ACTION_COUNT": 3000,
    "MAX_EXE_DURATION": 3600
}

# element cannot be clicked, from dom element tag

UNCLICKABLE_ANDROID_ELEMENT_LIST = [
    "android.widget.FrameLayout",
    "android.view.ViewGroup",
    "android.widget.LinearLayout"
]

# appium action setting

# bfs max swipe down count
MAX_SWIPE_DOWN_COUNT = 3

# dfs max depth
DFS_MAX_DEPTH = 10

# execution duration

EXECUTION_DURATION = 3600

# second
DEFAULT_WAITING_DURATION_AS_SECOND = 1

# millisecond
DEFAULT_WAITING_DURATION_AS_MILLISECOND = 1000

# appium settings
APPIUM_SERVER_IP = "0.0.0.0"
APPIUM_SERVER_PORT = "4723"
APPIUM_IOS_WDA_PORT = "8100"
APPIUM_NEW_COMMAND_TIMEOUT = 1800

# monkey mode default settings

MONKEY_ACTION_PERCENTAGE = {
    "PER_CLICK": 85,
    "PER_SWIPE_UP": 3,
    "PER_SWIPE_DOWN": 2,
    "PER_LONG_PRESS": 2,
    "PER_HOME_KEY": 2,
    "PER_BACK_KEY": 1,
    "PER_DOUBLE_CLICK": 2,
    "PER_PINCH": 1,
    "PER_UNPINCH": 2,
    "PER_DRAG": 1
}
