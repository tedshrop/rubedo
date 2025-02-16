from constants import *
import cv2
import numpy as np

def crop_frame(frame):
    mid_y = int(VIDEO_HEIGHT) // 2 + int(CROP_Y_OFFSET)
    mid_x = int(VIDEO_WIDTH) // 2 + int(CROP_X_OFFSET)
    half_y = int(CROP_FRAME_SIZE_Y) // 2
    half_x = int(CROP_FRAME_SIZE_X) // 2
    frame = frame[mid_y-half_y:mid_y+half_y, mid_x-half_x:mid_x+half_x]
    return frame


def preprocess_frame(frame):
    if frame is None or frame.size == 0:
        raise ValueError("Empty frame passed to preprocess_frame")
    lowerb = np.array([0, 0, 50])
    upperb = np.array([255, 255, 255])
    red_line = cv2.inRange(frame, lowerb, upperb)

    masked_video = cv2.bitwise_and(frame,frame,mask = red_line)

    gray = cv2.cvtColor(masked_video, cv2.COLOR_BGR2GRAY)
    return gray


def apply_gaussian_blur(frame):
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    return frame
