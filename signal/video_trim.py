import json
import os
import shutil
import math
import pandas as pd
import cv2
import glob
import numpy as np
import subprocess

real_path = os.path.join(os.path.curdir, 'REAL(1500)\\REAL_SENTENCE_morpheme')
syn_path = os.path.join(os.path.curdir, 'SYN(1500)\\SYN_SENTENCE_morpheme')

video = {}
video_data = {}

def shutil_video(v, s, e):
    mp4_s = 'ffmpeg - i input.mp4 - ss 00: 00:10 - to 00: 00:20 - c copy output.mp4'
    subprocess.check_call()
    # ffmpeg - i input.mp4 - ss 00: 00:10 - to 00: 00:20 - c copy output.mp4

def files_in_dir(target):
    arr = []
    files = os.listdir(target)
    for item in files:
        arr.append(os.path.join(target, item))

    return arr


def normalization(array):
    scale_array = array.copy()
    scale_array[::2] /= 2048
    scale_array[1::2] /= 1152
    return scale_array


if __name__ == '__main__':

    # Video to name labeling
    real_data = files_in_dir(real_path)
    syn_data = files_in_dir(syn_path)

    for data in real_data:
        with open(data, 'r', encoding='UTF-8') as f:
            data = f.read()
        jdata = json.loads(data)

        video[jdata['metaData']['name']] = jdata['data'][0]['attributes'][0]['name']

    # Video to data labeling
    for mp4 in video:
        if 'SEN' in mp4:
            openposed_data = files_in_dir(os.path.join(os.path.curdir, 'REAL(1500)\\REAL_SENTENCE_keypoints', mp4[:mp4.rfind('.')]))

            face_keypoints_2d_temp = []
            pose_keypoints_2d_temp = []
            hand_left_keypoints_2d_temp = []
            hand_right_keypoints_2d_temp = []
            face_keypoints_3d_temp = []
            pose_keypoints_3d_temp = []
            hand_left_keypoints_3d_temp = []
            hand_right_keypoints_3d_temp = []

            for keypoints in openposed_data:
                with open(keypoints, 'r') as f:
                    data = f.read()
                data = json.loads(data)
                face_keypoints_2d_temp.append(data['people']['face_keypoints_2d'])
                # pose_keypoints_2d_temp.append(data['people']['pose_keypoints_2d'])
                # hand_left_keypoints_2d_temp.append(data['people']['hand_left_keypoints_2d'])
                # hand_right_keypoints_2d_temp.append(data['people']['hand_right_keypoints_2d'])
                # face_keypoints_3d_temp.append(data['people']['face_keypoints_3d'])
                # pose_keypoints_3d_temp.append(data['people']['pose_keypoints_3d'])
                # hand_left_keypoints_3d_temp.append(data['people']['hand_left_keypoints_3d'])
                # hand_right_keypoints_3d_temp.append(data['people']['hand_right_keypoints_3d'])

            video_data[mp4] = [face_keypoints_2d_temp, pose_keypoints_2d_temp, hand_left_keypoints_2d_temp, hand_right_keypoints_2d_temp, face_keypoints_3d_temp, pose_keypoints_3d_temp, hand_left_keypoints_3d_temp, hand_right_keypoints_3d_temp]
            print(video_data)
            print(video_data[mp4][0])
            exit(1)
            # with open('test.txt', 'w') as f:
            #     json.dump(video_data, f)
            # exit(1)
