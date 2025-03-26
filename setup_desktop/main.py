import pyautogui
import os
from time import sleep
from dotenv import load_dotenv

from funcao_buscar_imagens import clica_na_imagem

load_dotenv()

SENHA_NOTION = os.getenv("SENHA_NOTION")
SENHA_GOOGLE = os.getenv("SENHA_GOOGLE")

#abrir o chrome e deixar na pagina de busca do google
clica_na_imagem('icone_chrome')
sleep(1)
pyautogui.hotkey("ctrl", "shift", "n")
sleep(2)
pyautogui.hotkey("ctrl", "l")
pyautogui.write("google", interval=0.10)
sleep(1)
pyautogui.press("space")
pyautogui.press("backspace")
pyautogui.press("enter")
sleep(2)
clica_na_imagem("icone_google")
sleep(4)

#abrir um site de notícias globo.com
pyautogui.hotkey("ctrl", "t")
pyautogui.hotkey("ctrl", "l")
pyautogui.write("globo.com", interval=0.10)
sleep(1)
pyautogui.press("space")
pyautogui.press("enter")
sleep(4)

#abrir a caixa de entrada de emails
pyautogui.hotkey("ctrl", "t")
pyautogui.hotkey("ctrl", "l")
pyautogui.write("gmail", interval=0.10)
sleep(1)
pyautogui.press("space")
pyautogui.press("enter")
sleep(3)
clica_na_imagem('icone_google_gmail')
sleep(4)
clica_na_imagem("botao_login_gmail")
sleep(5)
pyautogui.write("seuemail@email.com", interval=0.10)
pyautogui.press("enter")
sleep(2)
pyautogui.write(SENHA_GOOGLE, interval=0.10)
sleep(1)
pyautogui.press("enter")
sleep(4)

#abrir o calendario do google
pyautogui.hotkey("ctrl", "t")
pyautogui.hotkey("ctrl", "l")
pyautogui.write("google calendar", interval=0.10)
sleep(1)
pyautogui.press("space")
pyautogui.press("enter")
sleep(5)
clica_na_imagem("icone_google_calendar")
sleep(8)

#abrir a agenda no notion
pyautogui.hotkey("ctrl", "t")
pyautogui.hotkey("ctrl", "l")
pyautogui.write("notion", interval=0.10)
sleep(1)
pyautogui.press("space")
pyautogui.press("enter")
sleep(1)
clica_na_imagem("icone_notion")
sleep(5)
clica_na_imagem("botao_login_notion")
sleep(5)
pyautogui.write("seuemail@email.com", interval=0.10)
pyautogui.press("enter")
sleep(3)
pyautogui.write(SENHA_NOTION, interval=0.10)
pyautogui.press("enter")
sleep(3)

#abrir spotify e selecionar playlist lofi
clica_na_imagem("icone_spotify")
sleep(7)
clica_na_imagem("icone_busca_spotify")
sleep(1)
clica_na_imagem("campo_busca_spotify")
sleep(1)
pyautogui.write("lofi", interval=0.10)
sleep(2)
pyautogui.move(0, 300)
pyautogui.click()
sleep(2)
clica_na_imagem("icone_playlist_lofi")
sleep(3)
clica_na_imagem("icone_play")

#abrir o discord
clica_na_imagem("icone_discord")