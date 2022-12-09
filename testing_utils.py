import numpy as np
import cv2


def print_camera_properties(vid: cv2.VideoCapture):
    print('**********************************')
    print("FPS:", vid.get(cv2.CAP_PROP_FPS))
    print("BUFF_SIZE:", vid.get(cv2.CAP_PROP_BUFFERSIZE))
    print("WIDTH:", vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("HEIGHT:", vid.get(cv2.CAP_PROP_FRAME_HEIGHT))


def IR_camera_fix_black_frames_at_framebuffer(frame0: np.ndarray, frame1: np.ndarray, render_frame: np.ndarray):
    for i in range(360):
        for j in range(360):
            for k in range(3):
                v0 = frame0.item((i, j, k))
                v1 = frame1.item((i, j, k))
                render_frame.itemset((i, j, k), max(v0, v1))


def draw_align_lines(frame: np.ndarray, shape):
    row = shape[0]
    col = shape[1]
    divisor = 8
    for i in range(row):
        for j in range(col):

            ratio = max(row, col) // divisor
            pixel_painted = False
            for k in range(1, divisor):
                pixel_painted = (i == ratio * k) or (j == ratio * k)
                if pixel_painted:
                    break

            if pixel_painted:
                frame.itemset((i, j, 0), 0xFF)
                frame.itemset((i, j, 1), 0x00)
                frame.itemset((i, j, 2), 0x00)
