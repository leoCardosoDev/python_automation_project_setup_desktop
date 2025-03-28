import os
import pandas as pd
from dotenv import load_dotenv

from netflix import netflix_registro
from spotify import spotify_resgitro



load_dotenv()

#dados do cartao da empresa
NUMERO = os.getenv("NUMERO")
VALIDADE = os.getenv("VALIDADE")
CVV = os.getenv("CVV")
NOME = os.getenv("NOME")
SOBRENOME = os.getenv("SOBRENOME")

DADOS_CARTAO = {"numero": NUMERO, "validade": VALIDADE, "cvv" : CVV, "nome": NOME, "sobrenome": SOBRENOME}

#tratamento dos dados da lista de usuarios
dataframe_usuarios = pd.read_excel('usuarios.xlsx', skiprows=2)
dataframe_usuarios.columns = dataframe_usuarios.iloc[0]
dataframe_usuarios = dataframe_usuarios.tail(-1)
dataframe_usuarios["Nascimento"] = pd.to_datetime(dataframe_usuarios["Nascimento"])
dataframe_usuarios["Nascimento"] = dataframe_usuarios['Nascimento'].dt.strftime("%Y%m%d")

for indice, linha in dataframe_usuarios.iterrows():
    netflix_registro(
                    email=linha['Email'],
                    senha=linha['Senha'],
                    dados_cartao=DADOS_CARTAO
                    )
    spotify_resgitro(
                    email=linha['Email'],
                    senha=linha['Senha'],
                    usuario=linha['Usuario'],
                    cpf=linha['CPF'],
                    nascimento=linha['Nascimento'],
                    dados_cartao=DADOS_CARTAO,
                    genero=linha['Genero']
    )