import cv2
import numpy as np


def crop_RGB_image(image: np.ndarray):
    startY = 0
    endY = 480

    startX = 80
    endX = 540

    return image[startY:endY, startX:endX]


def resize_RGB_image(image: np.ndarray):
    return cv2.resize(image, (360, 360))


def merge_session_data_data(session_id : int):
    i = 0
    try:
        while True:
            img = cv2.imread(f'RawData/session_{session_id}/RGB/img{i}.png')
            cropped = crop_RGB_image(img)
            resized = resize_RGB_image(cropped)
            cv2.imwrite(f'ProcessedData/session_{session_id}/{i}_RGB.png', resized)
            img = cv2.imread(f'RawData/session_{session_id}/IR/img{i}.png', cv2.IMREAD_GRAYSCALE)
            cv2.imwrite(f'ProcessedData/session_{session_id}/{i}_IR.png', img)
            i += 1
    except:
        print(f"{i} image merged successfully.")
        return


class LabelTool:
    frameRGB: np.ndarray
    frameIR: np.ndarray

    def __init__(self):
        self.frameIR = np.zeros((360, 360, 1), dtype=np.uint8)
        self.frameRGB = np.zeros((360, 360, 3), dtype=np.uint8)









