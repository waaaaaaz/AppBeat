# coding: utf-8

import subprocess
import os

from utils import FileUtils


class CommandUtils:

    @staticmethod
    def cmd_format(cmd_str):
        return cmd_str.split(" ")

    @staticmethod
    def android_sdk_version(udid):
        cmd = "adb -s {0} shell getprop ro.build.version.sdk".format(udid)
        return CommandUtils.cmd_format(cmd)

    @staticmethod
    def android_platform_version(udid):
        cmd = "adb -s {0} shell getprop ro.build.version.release".format(udid)
        return CommandUtils.cmd_format(cmd)

    @staticmethod
    def ios_platform_version(udid):
        cmd = "ideviceinfo -u {0} -k ProductVersion".format(udid)
        return CommandUtils.cmd_format(cmd)

    @staticmethod
    def android_device_log(udid, log_name):
        cmd = "adb -s {0} logcat > {1}".format(udid, log_name)
        return CommandUtils.cmd_format(cmd)

    @staticmethod
    def ios_device_log(udid, log_name):
        cmd = "idevicesyslog -u {0} > {1}".format(udid, log_name)
        return CommandUtils.cmd_format(cmd)

    @staticmethod
    def is_android_process_exist(udid, process_name):
        cmd = "adb -s {0} shell ps | grep {1}".format(udid, process_name)
        return CommandUtils.cmd_format(cmd)

    @staticmethod
    def is_ios_process_exist(udid):
        report_dir = os.path.join(FileUtils.output_dir(udid), "screen_shot")
        FileUtils.make_dir(report_dir)
        cmd = "idevicecrashreport -u  {0} shell ps | grep {1}".format(udid, report_dir)
        return CommandUtils.cmd_format(cmd)

    @staticmethod
    def command_exe(cmd):
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, encoding='utf-8', universal_newlines=True)
        stdout, stderr = p.communicate()
        stdout = stdout.split('\n')[:-1]
        stderr = stderr.split("n")[:-1]
        return stdout, stderr
