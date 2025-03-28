import pyautogui
import calendar
from time import sleep

from funcoes_buscar_imagens import clica_na_imagem_spotify

def clique_mes(mes_nascimento):
    meses = {
        'January': 'imgs_spotify/opcao_janeiro.png',
        'February': 'imgs_spotify/opcao_fevereiro.png',
        'March': 'imgs_spotify/opcao_marco.png',
        'April': 'imgs_spotify/opcao_abril.png',
        'May': 'imgs_spotify/opcao_maio.png',
        'June': 'imgs_spotify/opcao_junho.png',
        'July': 'imgs_spotify/opcao_julho.png',
        'August': 'imgs_spotify/opcao_agosto.png',
        'September': 'imgs_spotify/opcao_setembro.png',
        'October': 'imgs_spotify/opcao_outubro.png',
        'November': 'imgs_spotify/opcao_novembro.png',
        'December': 'imgs_spotify/opcao_dezembro.png'
    }
    imagem_mes_nascimento = pyautogui.locateOnScreen(meses[mes_nascimento], confidence=0.9)

    return pyautogui.click(imagem_mes_nascimento)

def clique_genero(genero):
    generos = {
        'homem': 'imgs_spotify/opcao_genero_homem.png',
        'mulher': 'imgs_spotify/opcao_genero_mulher.png',
        'nao_binario': 'imgs_spotify/opcao_genero_nao_binario.png',
        'nao_informado': 'imgs_spotify/opcao_genero_nao_informado.png',
        'outro': 'imgs_spotify/opcao_genero_outro.png',
    }
    imagem_opcao_genero = pyautogui.locateOnScreen(generos[genero], confidence=0.9)

    return pyautogui.click(imagem_opcao_genero)

def spotify_resgitro(email, senha, usuario, cpf, nascimento, dados_cartao, genero):

    MES = calendar.month_name[int(nascimento[5:7])]

    #acesso ao navegador
    clica_na_imagem_spotify('icone_chrome')
    sleep(1)
    #abre nova guia anonima
    pyautogui.hotkey('ctrl', 'shift', 'n')
    sleep(2)
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.write('spotify', interval=0.10)
    pyautogui.press('space')
    pyautogui.press('enter')
    sleep(4)
    #acessa pagina spotify
    clica_na_imagem_spotify('link_spotify')
    sleep(4)
    #clica em 'inscreva-se'
    clica_na_imagem_spotify('botao_inscreva')
    sleep(6)
    #clica no campo de texto e insere email
    clica_na_imagem_spotify('campo_email')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(email, interval=0.1)
    #clica em 'seguinte'
    clica_na_imagem_spotify('botao_seguinte')
    sleep(1)
    #clica no campo de texto e insere uma senha
    clica_na_imagem_spotify('campo_senha')
    pyautogui.write(senha, interval=0.10)
    #clica em 'seguinte'
    clica_na_imagem_spotify('botao_seguinte')
    sleep(1)
     #clica no campo de texto e insere o Nome de usuario
    clica_na_imagem_spotify('campo_nome')
    pyautogui.write(usuario, interval=0.10)
    #preenche o campo do dia da data de nascimento
    clica_na_imagem_spotify('campo_dia_nascimento')
    pyautogui.write(nascimento[-2:], interval=0.10)
    #clica no dropdown para selecionar o mês da data de nascimento
    clica_na_imagem_spotify('campo_mes_nascimento')
    #clica no mês da data de nascimento
    sleep(1)
    clique_mes(MES)
    sleep(1)
    #preenche ano da data de nascimento
    clica_na_imagem_spotify('campo_ano_nascimento')
    pyautogui.write(nascimento[:4], interval=0.10)
    sleep(1)
    #seleciona genero
    clique_genero(genero)
    #clica em 'seguinte'
    clica_na_imagem_spotify('botao_seguinte')
    sleep(1)
    #concordar com termos e condições
    clica_na_imagem_spotify('opcao_concordo_com_termos')
    sleep(1)
    #clicar em registrar-se
    clica_na_imagem_spotify('botao_registrar')
    sleep(10)
    #Acessar aba Premium
    clica_na_imagem_spotify('botao_premium')
    sleep(3)
    #Ver planos
    clica_na_imagem_spotify('botao_ver_planos')
    sleep(1)
    #seleciona plano individual
    clica_na_imagem_spotify('card_plano_individual')
    pyautogui.scroll(-20)
    pyautogui.move(0, 310)
    pyautogui.click()
    sleep(3)
    #Clica no card da assinatura
    clica_na_imagem_spotify('card_assinatura_mensal')
    sleep(1)
    #Seleciona tipo de pagamento - cartão de crédito
    clica_na_imagem_spotify('card_cartao_credito')
    sleep(3)
    #desce um pouco a tela
    pyautogui.scroll(-400)
    sleep(4)
    #preenchimento das informações de pagamento
    clica_na_imagem_spotify('campo_num_cartao')
    pyautogui.write(dados_cartao['numero'], interval=0.10)
    clica_na_imagem_spotify('campo_validade_cartao')
    pyautogui.write(dados_cartao['validade'], interval=0.10)
    clica_na_imagem_spotify('campo_codigo_seguranca')
    pyautogui.write(dados_cartao['cvv'], interval=0.10)
    clica_na_imagem_spotify('campo_nome_cartao')
    pyautogui.write(dados_cartao['nome'] + dados_cartao['sobrenome'], interval=0.10)
    clica_na_imagem_spotify('campo_cpf_cartao')
    pyautogui.write(cpf, interval=0.10)
    #desce ate o fim da pagina
    pyautogui.scroll(-1000)
    #clica no botao compre agora
    clica_na_imagem_spotify('botao_comprar')
    sleep(5)
    #fecha a aba anonima
    pyautogui.hotkey('ctrl', 'w')
    sleep(2)
    #fecha a aba comum
    pyautogui.hotkey('ctrl', 'w')
    sleep(2)
