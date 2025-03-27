import pyautogui
from time import sleep

def clica_na_image_netflix(img):
    imagem = "imgs_netflix/" + img + '.png'
    sleep(1)
    local_imagem = pyautogui.locateOnScreen(imagem, confidence=0.8)
    return pyautogui.click(local_imagem)

def clica_na_image_spotify(img):
    imagem = "imgs_spotify/" + img + '.png'
    sleep(1)
    local_imagem = pyautogui.locateOnScreen(imagem, confidence=0.8)
    return pyautogui.click(local_imagem)

