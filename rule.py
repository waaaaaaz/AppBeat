# coding: utf-8

import yaml
import json
from setting import REQUIRED_ANDROID_CONFIG_FIELD, \
    REQUIRED_IOS_CONFIG_FIELD, \
    OPTIONAL_CONFIG_FIELD, \
    MONKEY_ACTION_PERCENTAGE, \
    TARGET_CONFIG_FIELD
from exception import ConfigError


class Rule(object):

    def __init__(self, device_type, mode, config_file, udid, exe_id):
        self.device_type = device_type
        self.config_file = config_file
        self.mode = mode
        self.udid = udid
        self.exe_id = exe_id
        self.config_dict = self.__config_file_load()
        self.__config_required_attr()
        self.__config_optional_attr()
        if self.mode == "monkey":
            self.__config_monkey_attr()
        if self.mode == "target":
            self.__config_target_attr()
        self.__del_attr()

    def __config_file_load(self):
        with open(self.config_file) as f:
            return yaml.safe_load(f)

    def __config_required_attr(self):
        if self.device_type == "android":
            for i in REQUIRED_ANDROID_CONFIG_FIELD:
                if i in self.config_dict["REQUIRED"].keys() and self.config_dict["REQUIRED"][i] is not None:
                    attr_name = i + "_REQUIRED"
                    attr_value = self.config_dict["REQUIRED"][i]
                    setattr(self, attr_name, attr_value)
                else:
                    raise ConfigError("no {0} field in configuration file, or which value is None".format(i))
        if self.device_type == "ios":
            for i in REQUIRED_IOS_CONFIG_FIELD:
                if i in self.config_dict["REQUIRED"].keys() and self.config_dict["REQUIRED"][i] is not None:
                    attr_name = i + "_REQUIRED"
                    attr_value = self.config_dict["REQUIRED"][i]
                    setattr(self, attr_name, attr_value)
                else:
                    raise ConfigError("no {0} field in configuration file, or which value is None".format(i))

    def __config_optional_attr(self):
        for i in OPTIONAL_CONFIG_FIELD.keys():
            if i in self.config_dict["OPTIONAL"].keys() and self.config_dict["OPTIONAL"][i] is not None:
                attr_value = self.config_dict["OPTIONAL"][i]
            else:
                attr_value = OPTIONAL_CONFIG_FIELD[i]
            attr_name = i + "_OPTIONAL"
            setattr(self, attr_name, attr_value)

    def __config_monkey_attr(self):
        attr_name = "MONKEY_PERCENTAGE"
        if "MONKEY_PERCENTAGE" in self.config_dict.keys() and isinstance(self.config_dict["MONKEY_PERCENTAGE"],
                                                                         dict):
            if len(self.config_dict["MONKEY_PERCENTAGE"]) > 0:
                monkey_percentage = {}
                for i in MONKEY_ACTION_PERCENTAGE.keys():
                    if i in self.config_dict["MONKEY_PERCENTAGE"].keys():
                        monkey_percentage[i] = self.config_dict["MONKEY_PERCENTAGE"][i]
                attr_value = monkey_percentage
        else:
            attr_value = MONKEY_ACTION_PERCENTAGE
        if self.mode == "ios" and "PER_HOME_KEY" in attr_value.keys():
            del attr_value["PER_HOME_KEY"]
        setattr(self, attr_name, attr_value)

    def __config_target_attr(self):
        if "TARGET" not in self.config_dict.keys():
            raise ConfigError("no target setting in config file")
        target_setting = []
        for i in self.config_dict["TARGET"]:
            target_item = {}
            for k, v in i.items():
                if k == "STEPS" and isinstance(v, list) is False and len(v) == 0:
                    raise ConfigError("illegal setting for steps")
                if k in TARGET_CONFIG_FIELD and v is not None:
                    target_item[k] = v
                if self.device_type == "ios" and k == "TARGET_ACTIVITY":
                    del target_item[k]
            target_item["COVERED"] = False
            target_setting.append(target_item)
        attr_name = "TARGET_SETTING"
        attr_value = target_setting
        setattr(self, attr_name, attr_value)

    def __del_attr(self):
        delattr(self, "config_dict")


if __name__ == "__main__":
    f = "/Users/shifang/Code/sqkb/AppBeat/config/example_config.yml"
    d = "android"
    m = "target"
    u = "259976a6"
    r = Rule(config_file=f, device_type=d, mode=m, udid=u)
    # print(json.dumps(r))
    print(json.dumps(r.__dict__))
