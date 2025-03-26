import pyautogui
import os
from time import sleep
from dotenv import load_dotenv

from setup_desktop.fuction_add_inage import add_image

load_dotenv()

SENHA_NOTION = os.getenv("SENHA_NOTION")
SENHA_GOOGLE = os.getenv("SENHA_GOOGLE")

add_image('icone_google')
