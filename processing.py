from constants import *
import cv2
import numpy as np

def crop_frame(frame):
    # Print the shape of the frame before cropping
    print(f"Original frame shape: {frame.shape}")

    mid_y = int(VIDEO_HEIGHT) // 2 + int(CROP_Y_OFFSET) //2
    mid_x = int(VIDEO_WIDTH) // 2 + int(CROP_X_OFFSET) //2
    half_y = int(CROP_FRAME_SIZE_Y) // 2
    half_x = int(CROP_FRAME_SIZE_X) // 2

    # Print the calculated values
    print(f"mid_y: {mid_y}, mid_x: {mid_x}, half_y: {half_y}, half_x: {half_x}")

    # Ensure the cropping indices are within the frame dimensions
    if mid_y - half_y < 0 or mid_y + half_y > frame.shape[0] or mid_x - half_x < 0 or mid_x + half_x > frame.shape[1]:
        raise ValueError("Cropping indices are out of frame bounds")

    frame = frame[mid_y-half_y:mid_y+half_y, mid_x-half_x:mid_x+half_x]

    # Print the shape of the frame after cropping
    print(f"Cropped frame shape: {frame.shape}")

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
