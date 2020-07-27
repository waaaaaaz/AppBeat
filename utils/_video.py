# coding: utf-8

import cv2
import os


class VideoUtils:

    @staticmethod
    def pic_to_video(pic_dir, display, exe_id):
        fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        video_name = pic_dir + os.path.sep + "{0}.avi".format(exe_id)
        # fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
        # video_name = pic_dir + os.path.sep + "{0}.mp4".format(exe_id)
        fps = 24
        rows = display[1]
        cols = display[0]
        display = (rows, cols)
        vvw = cv2.VideoWriter(video_name, fourcc, fps, display)
        frames_list = os.listdir(pic_dir)
        for i in range(0, len(frames_list)):
            frame_name = frames_list[i]
            if frame_name.endswith("png"):
                frame = cv2.imread(pic_dir + os.path.sep + frame_name)
                vvw.write(frame)
        return video_name


if __name__ == "__main__":
    pic_dir = "/Users/shifang/Code/sqkb/AppBeat/output/259976a6_20200722120238/screen_shot"
    display = (2030, 1080)
    exe_id = "90909"
    VideoUtils.pic_to_video(pic_dir, display, exe_id)
