import pyautogui
from time import sleep

from funcoes_buscar_imagens import clica_na_imagem_netflix

def netflix_registro(email, senha, dados_cartao):
    #acesso ao navegador
    clica_na_imagem_netflix('icone_chrome')
    sleep(1)
    #abre nova guia anonima
    pyautogui.hotkey('ctrl', 'shift', 'n')
    sleep(2)
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.write('netflix', interval=0.10)
    pyautogui.press('space')
    pyautogui.press('enter')
    sleep(4)
    #acessa pagina netflix
    clica_na_imagem_netflix('link_netflix')
    sleep(4)
    #clica no campo de texto, apaga o que tiver escrito e insere email
    clica_na_imagem_netflix('campo_email')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(email, interval=0.10)
    pyautogui.press('enter')
    sleep(2)
    #clica em proximo
    clica_na_imagem_netflix('botao_proximo_1')
    sleep(2)
    #clica no campo de texto e insere uma senha
    clica_na_imagem_netflix('campo_senha')
    pyautogui.write(senha, interval=0.10)
    pyautogui.press('enter')
    sleep(2)
    #clica em proximo
    clica_na_imagem_netflix('botao_proximo_2')
    sleep(2)
    #escolhe o plano
    clica_na_imagem_netflix('card_plano_padrao')
    sleep(1)
    #scroll até o final da pagina e clica em proximo
    pyautogui.scroll(-100)
    clica_na_imagem_netflix('botao_proximo_3')
    sleep(1)
    #seleciona forma de pagamento
    clica_na_imagem_netflix('card_cartao_credito')
    sleep(3)
    #preenchimento das informações de pagamento
    clica_na_imagem_netflix('campo_num_cartao')
    pyautogui.write(dados_cartao['numero'], interval=0.10)
    sleep(1)
    clica_na_imagem_netflix('campo_validade_cartao')
    pyautogui.write(dados_cartao['validade'], interval=0.10)
    sleep(1)
    clica_na_imagem_netflix('campo_codigo_seguranca_cartao')
    pyautogui.write(dados_cartao['cvv'], interval=0.10)
    sleep(1)
    clica_na_imagem_netflix('campo_nome_cartao')
    pyautogui.write(dados_cartao['nome'], interval=0.10)
    sleep(1)
    clica_na_imagem_netflix('opcao_cartao_credito')
    pyautogui.click()
    sleep(1)
    #scroll ate o final da pagina
    pyautogui.scroll(-300)
    clica_na_imagem_netflix('botao_iniciar_assinatura')
    #fecha guia anonima
    sleep(5)
    pyautogui.hotkey('ctrl', 'w')
    sleep(1)
    pyautogui.hotkey('ctrl', 'w')
    sleep(2)   

