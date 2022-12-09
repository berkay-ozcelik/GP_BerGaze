import os
import cv2
import numpy as np


def get_data_size():
    global directory_path
    lst = os.listdir(directory_path)
    return len(lst) // 2


def get_images():
    global directory_path, current_image_number
    img_RGB = cv2.imread(directory_path + f'{current_image_number}_RGB.png')
    img_IR = cv2.imread(directory_path + f'{current_image_number}_IR.png')
    return img_RGB, img_IR


def get_label():
    global label_directory_path, current_image_number

    try:
        file = open(label_directory_path + f'{current_image_number}_label.txt', 'r')
        raw_points = file.read()
        file.close()
        tokens = raw_points.split()
        x1, y1, x2, y2 = int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])
        return (x1, y1), (x2, y2)
    except:
        with open(label_directory_path + f'{current_image_number}_label.txt', 'w') as file:
            file.write('-1 -1 -1 -1')
        return (-1, -1), (-1, -1)


def left_mouse_button_pressed(x, y):
    global mouse_button_pressing, ref_point_of_rectangle
    if not mouse_button_pressing:
        mouse_button_pressing = True
        ref_point_of_rectangle = x, y


def left_mouse_button_unpressed(x, y):
    global mouse_button_pressing, end_point_of_rectangle
    if mouse_button_pressing:
        mouse_button_pressing = False
        end_point_of_rectangle = x, y


def mouse_moved(x, y):
    global mouse_button_pressing
    global IR_frame_that_window_contains, IR_original_frame
    global RGB_frame_that_window_contains, RGB_original_frame

    if not mouse_button_pressing:
        return
    IR_frame_that_window_contains = IR_original_frame.copy()
    RGB_frame_that_window_contains = RGB_original_frame.copy()

    cv2.rectangle(IR_frame_that_window_contains, ref_point_of_rectangle, (x, y), (0xFF, 0, 0), 2)
    cv2.rectangle(RGB_frame_that_window_contains, ref_point_of_rectangle, (x, y), (0xFF, 0, 0), 2)


def mouse_callback_adapter(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        left_mouse_button_pressed(x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        left_mouse_button_unpressed(x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        mouse_moved(x, y)


def set_label(remove=False):
    global label_directory_path, current_image_number, ref_point_of_rectangle, end_point_of_rectangle

    if remove:
        ref_point_of_rectangle = (-1, -1)
        end_point_of_rectangle = (-1, -1)
    file = open(label_directory_path + f'{current_image_number}_label.txt', 'w')
    x1, y1 = ref_point_of_rectangle
    x2, y2 = end_point_of_rectangle
    line = f'{x1} {y1} {x2} {y2}'
    file.write(line)
    file.close()


def load_data():
    global mouse_button_pressing, RGB_original_frame, IR_original_frame, current_image_number
    global ref_point_of_rectangle, end_point_of_rectangle
    global ref_point_rect_original, end_point_rect_original
    mouse_button_pressing = False
    RGB_original_frame, IR_original_frame = get_images()
    ref_point_of_rectangle, end_point_of_rectangle = get_label()
    ref_point_rect_original = ref_point_of_rectangle
    end_point_rect_original = end_point_of_rectangle
    RGB_frame_cpy = RGB_original_frame.copy()
    IR_frame_cpy = IR_original_frame.copy()

    cv2.rectangle(RGB_frame_cpy, ref_point_rect_original, end_point_of_rectangle, (0, 0, 0xFF), 2)
    cv2.rectangle(IR_frame_cpy, ref_point_rect_original, end_point_of_rectangle, (0, 0, 0xFF), 2)

    return RGB_frame_cpy, IR_frame_cpy


mouse_button_pressing = False
RGB_original_frame: np.ndarray
RGB_frame_that_window_contains: np.ndarray

IR_original_frame: np.ndarray
IR_frame_that_window_contains: np.ndarray

ref_point_rect_original = (int, int)
end_point_rect_original = (int, int)

ref_point_of_rectangle: (int, int)
end_point_of_rectangle: (int, int)

# TODO: Add real data path and session id
directory_path = f'ProcessedData/images/'
label_directory_path = f'ProcessedData/labels/'

current_image_number = 0
total_dataset_length = get_data_size()

window_name = 'LabelTool'
win_name_rgb = window_name + 'RGB'
win_name_ir = window_name + 'IR'

cv2.namedWindow(win_name_rgb)
cv2.namedWindow(win_name_ir)

cv2.setMouseCallback(win_name_ir, mouse_callback_adapter)
cv2.setMouseCallback(win_name_rgb, mouse_callback_adapter)

IR_frame_that_window_contains, RGB_frame_that_window_contains = load_data()

while (True):
    cv2.imshow(win_name_ir, IR_frame_that_window_contains)
    cv2.imshow(win_name_rgb, RGB_frame_that_window_contains)

    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q'):
        break

    elif key_pressed == ord('n'):
        label_changed = not (
                end_point_of_rectangle == end_point_rect_original and ref_point_of_rectangle == ref_point_rect_original)
        if label_changed:
            set_label()
        if current_image_number < total_dataset_length - 1:
            current_image_number += 1
        else:
            current_image_number = 0

        RGB_frame_that_window_contains, IR_frame_that_window_contains = load_data()

    elif key_pressed == ord('p'):
        if current_image_number > 0:
            current_image_number -= 1
        else:
            current_image_number = total_dataset_length - 1

        RGB_frame_that_window_contains, IR_frame_that_window_contains = load_data()

    elif key_pressed == ord('c'):
        set_label(remove=True)
        RGB_frame_that_window_contains, IR_frame_that_window_contains = load_data()

cv2.destroyAllWindows()
