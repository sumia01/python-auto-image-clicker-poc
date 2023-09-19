import logging
import os
import sys
import cv2
import numpy as np
import pyautogui
import time
import logging

UP_AND_FLUSH = '\033[F\r\033[K'
LOGPATH = "./logs"
LOGFILE = f"{LOGPATH}/{time.time()}.log"
SCREENSHOT = './data/screenshot.png'
DEFAULT_REFERENCE = './data/reference.png'
DIFF_METHOD = cv2.TM_SQDIFF_NORMED


def setupLogger():
    if not os.path.exists(LOGPATH):
        os.makedirs(LOGPATH)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[
            logging.FileHandler(LOGFILE),
            logging.StreamHandler()
        ]
    )


def askForReference() -> str:
    referenceLocation = ""
    # check if there is a reference arg
    if len(sys.argv) > 1:
        referenceLocation = sys.argv[1]

    if referenceLocation == "":
        referenceLocation = DEFAULT_REFERENCE

    return referenceLocation


def wait(seconds: int = 2):
    # print a text with the countdown
    for i in range(seconds, 0, -1):
        print(f"waiting {i} second(s)", end=' \r', flush=True)

        time.sleep(1)


def takeScreenshot():
    logging.info("taking screenshot...")
    image = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

    cv2.imwrite(SCREENSHOT, image)


def findButtonCenter(reference):
    screenshot = cv2.imread(SCREENSHOT)

    # We want the minimum squared difference
    result = cv2.matchTemplate(reference, screenshot, DIFF_METHOD)
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    # exit if the confidence is too low
    if mn > 0.1:
        return (False, None)

    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx, MPy = mnLoc

    # Step 2: Get the size of the template. This is the same size as the match.
    trows, tcols = reference.shape[:2]

    # Step 3: Draw the rectangle on large_imagepz
    cv2.rectangle(screenshot, (MPx, MPy),
                  (MPx+tcols, MPy+trows), (0, 0, 255), 2)

    # get the center coordinates of the rectangle
    center = (MPx+tcols/2, MPy+trows/2)

    return (True, center)


def main():
    referenceLocation = askForReference()

    if not os.path.exists(referenceLocation):
        logging.error(f"reference image not found at {referenceLocation}")
        sys.exit(1)

    reference = cv2.imread(referenceLocation)

    while True:
        wait(5)
        takeScreenshot()

        (found, center) = findButtonCenter(reference)
        if found:
            pyautogui.click(center)
            logging.info(f"button found and clicked at location: {center}")


if __name__ == "__main__":
    setupLogger()
    main()
