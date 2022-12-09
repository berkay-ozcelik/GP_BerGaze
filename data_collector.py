import os.path
import time

import cv2
import testing_utils as utils
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from enum import IntEnum
import numpy as np


class VideoDevice(IntEnum):
    RGB = 0
    IR = 2


class IR_Camera(Process):
    conn: Connection
    frame: np.ndarray
    session_id: int

    def __init__(self, conn: Connection, session_id: int):
        super().__init__()
        self.conn = conn
        self.frame = np.zeros(shape=(360, 360, 3), dtype=np.uint8)
        self.session_id = session_id

    def run(self) -> None:
        video_src = cv2.VideoCapture(VideoDevice.IR)
        video_src.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        utils.print_camera_properties(video_src)

        frame_id = 0

        while True:
            self.conn.send(0x0)
            _, frame0 = video_src.read()
            _, frame1 = video_src.read()

            utils.IR_camera_fix_black_frames_at_framebuffer(frame0, frame1, self.frame)

            cv2.imshow('IR', self.frame)

            cv2.imwrite(f"RawData/session_{self.session_id}/IR/img{frame_id}.png", self.frame)
            frame_id += 1

            cv2.waitKey(1)


class RGB_Camera(Process):
    conn: Connection
    frame: np.ndarray
    session_id: int

    def __init__(self, conn: Connection, session_id: int):
        super().__init__()
        self.conn = conn
        self.frame = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        self.session_id = session_id

    def run(self) -> None:
        video_src = cv2.VideoCapture(VideoDevice.RGB)
        video_src.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        utils.print_camera_properties(video_src)

        frame_id = 0
        while True:
            self.conn.recv()
            video_src.grab()

            video_src.retrieve(self.frame)

            cv2.imshow('RGB', self.frame)
            cv2.imwrite(f"RawData/session_{self.session_id}/RGB/img{frame_id}.png", self.frame)
            frame_id += 1

            cv2.waitKey(1)


def get_session_id():
    s_id = 0
    while True:
        path = f"RawData/session_{s_id}"
        if os.path.exists(path):
            s_id += 1
        else:
            return s_id


def create_path_for_subject(s_id: int):
    path = f"RawData/session_{s_id}"
    os.mkdir(path)

    path = f"RawData/session_{s_id}/RGB"
    os.mkdir(path)

    path = f"RawData/session_{s_id}/IR"
    os.mkdir(path)

    print(f'Folder created for session_{s_id}')


session_id = get_session_id()
create_path_for_subject(session_id)

conn_IR, conn_RGB = Pipe(True)
IR = IR_Camera(conn_IR, session_id)
RGB = RGB_Camera(conn_RGB, session_id)

RGB.start()
IR.start()

time.sleep(2)

input('->')

RGB.kill()
IR.kill()
