import pyautogui
from time import sleep


def add_image(img):
    image = 'imgs/'+ img + '.png'
    sleep(1)
    local_image = pyautogui.locateOnScreen(image, confidence=0.9)
    return pyautogui.click(local_image)