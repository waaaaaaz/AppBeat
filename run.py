# coding: utf-8

import argparse
import sys

from log import Log
from builder import Builder
from utils import FileUtils
from setting import EXECUTION_MODE

# script_path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
logger = Log.logger(__file__)


def parse_options():
    parser = argparse.ArgumentParser(usage="app遍历工具执行入口")

    parser.add_argument(
        '-T',
        '--type',
        help="device type: android or ios"
    )

    parser.add_argument(
        '-U',
        '--udid',
        help="device serial: udid"
    )

    parser.add_argument(
        '-M',
        '--mode',
        help="execution mode: bfs/ dfs/ monkey/ target"
    )

    parser.add_argument(
        '-F',
        '--config',
        help="yaml config file path"
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_options()
    print(args)
    device_type = args.type.lower()
    device_udid = args.udid
    execution_mode = args.mode.lower()
    config_file = args.config

    if device_type is None or device_type not in ["android", "ios"]:
        print("device type 参数指定错误; 使用 --help 命令查看详情")
        sys.exit(1)

    if device_udid is None:
        print("device udid 参数指定错误; 使用 --help 命令查看详情")
        sys.exit(1)

    if execution_mode is None or execution_mode not in EXECUTION_MODE:
        print("execution mode 参数指定错误; 使用 --help 命令查看详情")
        sys.exit(1)

    if config_file is None or FileUtils.file_available(config_file) is False:
        print("config file 参数指定错误; 使用 --help 命令查看详情")
        sys.exit(1)

    logger.info("config: device type is {0}".format(device_type))
    logger.info("config: device udid is {0}".format(device_udid))
    logger.info("config: execution mode is {0}".format(execution_mode))
    logger.info("config: yaml config file is {0}".format(config_file))

    builder = Builder(config_file=config_file, udid=device_udid, mode=execution_mode, device_type=device_type)
    builder.exe()


if __name__ == "__main__":
    main()
