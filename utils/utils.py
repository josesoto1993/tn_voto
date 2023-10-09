import datetime
import logging
import random
from typing import Tuple, Optional

import cv2
import numpy as np
import pyautogui
from PIL import Image

DATA_FOLDER = "data/"
ERROR_FOLDER = "errors"

BASE_SCREENSHOT_NAME = 'screenshot.png'

RETRIES_TO_LOAD = 5
MAX_CLOSE_RETRIES = 20

GENERAL_FOLDER = "data/general"
BTN_X_FOLDER = GENERAL_FOLDER + "/btn_x"
CONTINUE_FOLDER = GENERAL_FOLDER + "/continue"
INTERRUPT_FOLDER = GENERAL_FOLDER + "/interrupt"

logging.basicConfig(level=logging.INFO)


def image_on_screen(img_str: str,
                    precision=0.8,
                    screenshot: Image = None,
                    gray_scale=True) -> Tuple[bool, Optional[Tuple[int, int]], Optional[float]]:
    if screenshot is None:
        screenshot = pyautogui.screenshot()

    img_rgb = np.array(screenshot)

    # Check if we need to convert image to grayscale
    if gray_scale:
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(img_str, 0)
    else:
        template = cv2.imread(img_str)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    logging.debug(f"path: {img_str}, max_val: {max_val}")

    if max_val < precision:
        return False, None, max_val
    else:
        return True, max_loc, max_val


def find_image_and_click(
        filepaths: list[str],
        msg=None,
        precision=0.8,
        screenshot=None,
        gray_scale=True,
        retries=RETRIES_TO_LOAD,
        error_filename=None
):
    for _ in range(retries):
        on_screen, position, _, best_match_filepath = any_image_on_screen(
            filepaths,
            precision=precision,
            screenshot=screenshot,
            gray_scale=gray_scale
        )

        if on_screen:
            if msg:
                logging.debug(f"Select: {msg} - best image is: {best_match_filepath}")
            click_on_rect_area(top_left_corner=position, filepath=best_match_filepath)
            return

    _find_image_and_click_log_error(filepaths, msg=msg, filename=error_filename)


def any_image_on_screen(paths_array: list[str],
                        precision=0.8,
                        screenshot=None,
                        gray_scale=True) -> Tuple[bool, Optional[Tuple[int, int]], Optional[float], Optional[str]]:
    best_max_val = None
    best_max_loc = None
    best_image = None
    if screenshot is None:
        screenshot = pyautogui.screenshot()

    for img_str in paths_array:
        on_screen, max_loc, max_val = image_on_screen(img_str,
                                                      precision=precision,
                                                      screenshot=screenshot,
                                                      gray_scale=gray_scale)

        if on_screen and (best_max_val is None or max_val > best_max_val):
            best_max_val = max_val
            best_max_loc = max_loc
            best_image = img_str

    if best_image is None:
        return False, None, None, None
    else:
        return True, best_max_loc, best_max_val, best_image


def _find_image_and_click_log_error(filepaths, msg, filename=None):
    if filename is None:
        filename = timestamped_filename(filename=ERROR_FOLDER + "/error_find_and_click")
    else:
        filename = ERROR_FOLDER + "/" + filename
    get_screenshot(save=True, filename=filename)
    msg = msg or "the image"
    raise ImageNotFoundException(f"Fail select: {msg}, for images {filepaths}")


def get_screenshot(save=False, filename=BASE_SCREENSHOT_NAME) -> Image:
    logging.debug("get_screenshot")
    screenshot = pyautogui.screenshot()
    if save:
        save_screenshot(filename, screenshot)
    return screenshot


def save_screenshot(filename, screenshot):
    if '.' not in filename:
        filename += '.png'
    screenshot.save(DATA_FOLDER + filename)
    logging.debug(f"Screenshot captured and saved as {filename}.")


def timestamped_filename(filename="") -> str:
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y%m%d_%H%M%S")
    return f"{filename}_{formatted_time}"


def click_on_rect_area(top_left_corner, size=None, filepath=None):
    if size is None and filepath is None:
        raise ValueError("Cannot use size and filepath as None at the same time")

    x, y = top_left_corner

    width = 0
    height = 0

    if size:
        width, height = size

    if filepath:
        width, height = get_image_size(filepath)

    # Calculate the random position within the rectangle
    random_x = x + random.uniform(0, width)
    random_y = y + random.uniform(0, height)

    # Move the mouse to the random position and click
    pyautogui.moveTo(random_x, random_y)
    pyautogui.click()


def get_image_size(image_path: str) -> Tuple[int, int]:
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height


class ImageNotFoundException(Exception):
    pass
