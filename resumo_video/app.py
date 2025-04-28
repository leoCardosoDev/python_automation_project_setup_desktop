import os
import re
import shutil
import tempfile
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment


# -------------------------
# CONFIGURAÇÃO E SEGURANÇA
# -------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(
    page_title="YouTube Vídeo para Resumo em Markdown",
    layout="centered"
)

# -------------------------
# FUNÇÕES AUXILIARES
# -------------------------

def instrucoes():
    st.markdown("""
    ## 🎬 YouTube Vídeo para Resumo Markdown
    1. Insira a URL de um vídeo público do YouTube.
    2. Aguarde enquanto o vídeo é baixado, convertido, transcrito e resumido.
    3. Baixe o arquivo `.md` gerado com tópicos principais do vídeo.
    ---
    """)

def baixar_video_ytdlp(url, pasta_destino):
    """Baixa apenas o vídeo do YouTube e retorna o caminho e título."""
    try:
        import yt_dlp

        ydl_opts = {
            'format': 'best[ext=mp4]/best',  # Prioriza MP4, mas aceita outros formatos se necessário
            'outtmpl': str(Path(pasta_destino) / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info['title']
            # Limpa o título para uso em nomes de arquivo
            titulo_limpo = re.sub(r'[^a-zA-Z0-9_\-]', '_', titulo)
            # Obtém o caminho do arquivo baixado
            arquivo_baixado = str(Path(pasta_destino) / f"{titulo}.mp4")
            if not Path(arquivo_baixado).exists():
                # Tenta encontrar o arquivo real se o nome não for exatamente como esperado
                arquivos = list(Path(pasta_destino).glob("*"))
                if arquivos:
                    arquivo_baixado = str(arquivos[0])

            return arquivo_baixado, titulo
    except Exception as e:
        raise ValueError(f"Erro ao baixar vídeo com yt-dlp: {e}")

def converter_video_para_mp3(path_video, pasta_destino):
    """Converte arquivo de vídeo em MP3, retorna caminho."""
    try:
        audio = AudioSegment.from_file(path_video)
        mp3_path = str(Path(pasta_destino) / (Path(path_video).stem + '.mp3'))
        audio.export(mp3_path, format="mp3")
        return mp3_path
    except Exception as e:
        raise ValueError(f"Falha na conversão para mp3: {e}")

def transcrever_audio_whisper(path_mp3, model="whisper-1", language="pt", response_format="text"):
    with open(path_mp3, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model=model,
            file=f,
            language=language,
            response_format=response_format
        )
    return transcript

def solicitar_resumo_openai(texto, titulo):
    """Usa a OpenAI API para gerar um resumo detalhado."""
    prompt = (
        "Resuma detalhadamente o conteúdo do vídeo do YouTube a seguir.\n"
        f"Título: {titulo}\n"
        "Retorne como Markdown com os seguintes tópicos:\n"
        "- Lista dos principais temas tratados\n"
        "- Observações adicionais se relevante\n\n"
        "Vídeo transcrito:\n"
        f"{texto}\n\n"
        "Resumo em Markdown:"
    )
    try:
        response = client.chat.completions.create(model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente de resumos de vídeos em português."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4)
        resumo = response.choices[0].message.content.strip()
        return resumo
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar resumo com OpenAI: {e}")

def salvar_md(resumo_md, titulo, pasta_destino):
    """Salva o markdown do resumo em arquivo e retorna caminho."""
    try:
        nome_base = re.sub(r'[^a-zA-Z0-9_\-]', '_', titulo)[:40]
        filename = f"{nome_base}_resumo.md"
        full_path = Path(pasta_destino) / filename
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(resumo_md)
        return str(full_path)
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar arquivo Markdown: {e}")

# -------------------------
# INTERFACE DO USUÁRIO
# -------------------------

def main():
    instrucoes()
    url = st.text_input("🔗 Cole a URL do vídeo do YouTube aqui:", "")

    if st.button("Gerar Resumo em Markdown", type="primary") and url:
        with st.spinner("Criando ambiente temporário..."):
            tmpdir = tempfile.mkdtemp()
            try:
                # Download do vídeo
                st.info("🔽 Baixando vídeo do YouTube...")
                path_video, titulo = baixar_video_ytdlp(url, Path(tmpdir))
                st.success("Download concluído!")

                # Conversão para MP3 (se necessário)
                st.info("🔄 Convertendo arquivo para MP3...")
                path_mp3 = converter_video_para_mp3(path_video, Path(tmpdir))
                st.success("Conversão para áudio concluída!")

                # Transcrição automática
                st.info("📝 Transcrevendo áudio com Whisper...")
                texto_transcrito = transcrever_audio_whisper(path_mp3)
                st.success("Transcrição concluída!")

                # Requisição de resumo detalhado à OpenAI
                st.info("💡 Enviando transcrição para geração de resumo...")
                resumo_md = solicitar_resumo_openai(texto_transcrito, titulo)
                st.success("Resumo gerado com sucesso!")

                # Salvando o Markdown
                st.info("💾 Salvando o resumo markdown...")
                caminho_md = salvar_md(resumo_md, titulo, tmpdir)
                st.success("Arquivo Markdown salvo!")

                # Exibição dos resultados
                st.markdown(f"### 📄 Resumo de: **{titulo}**")
                st.markdown(resumo_md)
                with open(caminho_md, "rb") as fp:
                    st.download_button(
                        label="⬇️ Baixar resumo em Markdown",
                        data=fp,
                        file_name=Path(caminho_md).name,
                        mime="text/markdown"
                    )
            except Exception as e:
                st.error(str(e))
            finally:
                shutil.rmtree(tmpdir)

    st.markdown("---")
    st.caption("🔒 Sua chave OpenAI está segura e nunca é exposta neste app. | Desenvolvido para Streamlit Cloud.")

if __name__ == "__main__":
    main()