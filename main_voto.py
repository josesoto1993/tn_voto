import logging
import time

from utils.utils import image_on_screen, find_image_and_click, get_screenshot, ImageNotFoundException

FILES_FOLDER = "data/"

SLEEP_DURATION = 3
CAN_VOTE_IMG_PATH = FILES_FOLDER + "vote_btn.png"
VOTE_IMG_PATH = [CAN_VOTE_IMG_PATH]
ALREADY_VOTE_IMG_PATH = FILES_FOLDER + "page_loaded.png"
RELOAD_IMG_PATH = [(FILES_FOLDER + "reload_btn.png")]

logging.root.setLevel(logging.INFO)


def main():
    while True:
        await_response()
        screenshot = get_screenshot(save=True)
        handle_vote_loop(screenshot)


def handle_vote_loop(screenshot):
    if can_vote(screenshot):
        vote(screenshot)
    elif already_vote(screenshot):
        reload(screenshot)
    else:
        logging.info("Ni se voto ni se puede votar")


def await_response():
    logging.info(f"sleep for: {SLEEP_DURATION} sec")
    time.sleep(SLEEP_DURATION)


def can_vote(screenshot):
    on_screen, _, _ = image_on_screen(CAN_VOTE_IMG_PATH,
                                      screenshot=screenshot)
    return on_screen


def vote(screenshot):
    logging.info("se puede votar, intentando votar")
    find_image_and_click(VOTE_IMG_PATH,
                         screenshot=screenshot,
                         msg="vote btn",
                         error_filename="fail_vote")


def already_vote(screenshot):
    on_screen, _, _ = image_on_screen(ALREADY_VOTE_IMG_PATH,
                                      screenshot=screenshot)
    return on_screen


def reload(screenshot):
    logging.info("ya se voto, recargando")
    try:
        find_image_and_click(RELOAD_IMG_PATH,
                             screenshot=screenshot,
                             msg="reload btn",
                             error_filename="fail_reload")
    except ImageNotFoundException:
        logging.info("ya esta recargando, sigue aguarndando")


if __name__ == "__main__":
    main()
