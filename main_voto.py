import logging
import time

from utils.utils import image_on_screen, find_image_and_click, get_screenshot, ImageNotFoundException, DATA_FOLDER

INITIAL_DELAY = 15
SLEEP_DURATION = 3
INITIAL_SCREEN = "initial_screen.png"
CAN_VOTE_IMG_PATH = DATA_FOLDER + "vote_btn.png"
VOTE_IMG_PATH = [CAN_VOTE_IMG_PATH]
ALREADY_VOTE_IMG_PATH = DATA_FOLDER + "page_loaded.png"
RELOAD_IMG_PATH = [(DATA_FOLDER + "reload_btn.png")]

logging.root.setLevel(logging.INFO)


def main():
    await_response(INITIAL_DELAY)
    get_screenshot(save=True, filename=INITIAL_SCREEN)
    while True:
        await_response(SLEEP_DURATION)
        screenshot = get_screenshot()
        handle_vote_loop(screenshot)


def handle_vote_loop(screenshot):
    if can_vote(screenshot):
        vote(screenshot)
    elif already_vote(screenshot):
        reload(screenshot)
    else:
        logging.info("Ni se voto ni se puede votar")


def await_response(sleep_time=SLEEP_DURATION):
    logging.info(f"sleep for: {sleep_time} sec")
    time.sleep(sleep_time)


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
