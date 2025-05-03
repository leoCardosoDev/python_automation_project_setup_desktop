import os
import re
import shutil
import tempfile
import time
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

def verificar_duracao_video(path_mp3, duracao_maxima_minutos=10):
    """Verifica se o vídeo é muito longo e avisa o usuário."""
    audio = AudioSegment.from_file(path_mp3)
    duracao_minutos = len(audio) / (1000 * 60)  # Converte de milissegundos para minutos
    
    if duracao_minutos > duracao_maxima_minutos:
        st.warning(f"⚠️ O vídeo tem {duracao_minutos:.1f} minutos, o que pode resultar em um processamento lento e possíveis erros.")
        st.info("Para melhores resultados, considere processar vídeos de até 10 minutos.")
        return True, duracao_minutos
    return False, duracao_minutos

def dividir_audio(path_mp3, pasta_destino, duracao_segmento=15, max_file_size_bytes=25*1024*1024):
    """Divide o áudio em segmentos menores para facilitar a transcrição.
    
    Args:
        path_mp3: Caminho para o arquivo MP3
        pasta_destino: Pasta onde os segmentos serão salvos
        duracao_segmento: Duração de cada segmento em segundos
        max_file_size_bytes: Tamanho máximo de cada arquivo em bytes (25MB por padrão)
    
    Returns:
        Lista de caminhos para os segmentos
    """
    try:
        audio = AudioSegment.from_file(path_mp3)
        segmentos = []
        
        # Converte duração para milissegundos
        duracao_ms = duracao_segmento * 1000
        
        # Calcula o número de segmentos
        num_segmentos = len(audio) // duracao_ms + (1 if len(audio) % duracao_ms > 0 else 0)
        
        for i in range(num_segmentos):
            inicio = i * duracao_ms
            fim = min((i + 1) * duracao_ms, len(audio))
            
            segmento = audio[inicio:fim]
            segmento_path = str(Path(pasta_destino) / f"segmento_{i:03d}.mp3")
            
            # Exporta com qualidade reduzida para diminuir o tamanho do arquivo
            segmento.export(
                segmento_path, 
                format="mp3",
                bitrate="64k",  # Bitrate mais baixo para reduzir tamanho
                parameters=["-ac", "1"]  # Converte para mono
            )
            
            # Verifica o tamanho do arquivo
            file_size = Path(segmento_path).stat().st_size
            if file_size > max_file_size_bytes:
                st.warning(f"Segmento {i+1} excede o limite de tamanho. Reduzindo qualidade...")
                # Se ainda estiver muito grande, reduz ainda mais a qualidade
                segmento.export(
                    segmento_path, 
                    format="mp3",
                    bitrate="32k",  # Bitrate ainda mais baixo
                    parameters=["-ac", "1"]  # Mono
                )
            
            segmentos.append(segmento_path)
        
        return segmentos
    except Exception as e:
        raise ValueError(f"Erro ao dividir áudio: {e}")

def transcrever_segmentos(segmentos, max_retries=3, max_file_size_bytes=25*1024*1024):
    """Transcreve múltiplos segmentos de áudio e combina os resultados.
    
    Args:
        segmentos: Lista de caminhos para os segmentos de áudio
        max_retries: Número máximo de tentativas por segmento
        max_file_size_bytes: Tamanho máximo permitido para cada arquivo
    
    Returns:
        Texto transcrito completo
    """
    transcricao_completa = []
    
    total_segmentos = len(segmentos)
    progress_bar = st.progress(0, text=f"Transcrevendo 0/{total_segmentos} segmentos")
    
    for idx, segmento_path in enumerate(segmentos):
        progress_text = f"Transcrevendo segmento {idx+1}/{total_segmentos}"
        progress_value = (idx / total_segmentos)
        progress_bar.progress(progress_value, text=progress_text)
        # Verifica o tamanho do arquivo
        file_size = Path(segmento_path).stat().st_size
        if file_size > max_file_size_bytes:
            st.warning(f"Segmento {idx+1} ainda excede o limite de tamanho ({file_size/1024/1024:.2f} MB). Tentando reduzir mais...")
            # Carrega o segmento
            segmento_audio = AudioSegment.from_file(segmento_path)
            # Reduz ainda mais a qualidade
            segmento_audio.export(
                segmento_path, 
                format="mp3",
                bitrate="16k",  # Bitrate muito baixo para garantir tamanho reduzido
                parameters=["-ac", "1", "-ar", "16000"]  # Mono e taxa de amostragem reduzida
            )
            
            # Verifica novamente o tamanho
            file_size = Path(segmento_path).stat().st_size
            if file_size > max_file_size_bytes:
                st.error(f"Não foi possível reduzir o segmento {idx+1} abaixo do limite. Pulando...")
                transcricao_completa.append("[Segmento muito grande para transcrição]")
                continue
        
        for tentativa in range(max_retries):
            try:
                with open(segmento_path, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="pt"
                    )
                
                transcricao_completa.append(transcript.text)
                break  # Sai do loop de tentativas se bem-sucedido
            except Exception as e:
                error_msg = str(e)
                if "413" in error_msg and tentativa < max_retries - 1:
                    st.warning(f"Arquivo muito grande. Tentando reduzir mais o segmento {idx+1}...")
                    
                    # Tenta reduzir ainda mais a qualidade
                    segmento_audio = AudioSegment.from_file(segmento_path)
                    segmento_audio.export(
                        segmento_path, 
                        format="mp3",
                        bitrate="8k",  # Bitrate extremamente baixo
                        parameters=["-ac", "1", "-ar", "8000"]  # Mono e taxa de amostragem muito baixa
                    )
                elif tentativa == max_retries - 1:  # Última tentativa
                    st.warning(f"Falha ao transcrever segmento {idx+1}: {e}")
                    transcricao_completa.append("[Falha na transcrição deste segmento]")
                else:
                    time.sleep(2)  # Pequena pausa antes de tentar novamente
    
    progress_bar.progress(1.0, text=f"Transcrição concluída! {total_segmentos}/{total_segmentos} segmentos")
    return " ".join(transcricao_completa)

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
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente de resumos de vídeos em português."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
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

                # Conversão para MP3
                st.info("🔄 Convertendo arquivo para MP3...")
                path_mp3 = converter_video_para_mp3(path_video, Path(tmpdir))
                st.success("Conversão para áudio concluída!")
                
                # Verifica a duração do vídeo
                video_longo, duracao_minutos = verificar_duracao_video(path_mp3)
                
                # Ajusta a duração do segmento com base na duração total do vídeo
                duracao_segmento = 10  # Padrão para vídeos curtos
                if duracao_minutos > 30:
                    duracao_segmento = 5  # Segmentos mais curtos para vídeos muito longos
                elif duracao_minutos > 10:
                    duracao_segmento = 8  # Segmentos intermediários para vídeos médios
                
                # Dividir o áudio em segmentos
                st.info("✂️ Dividindo áudio em segmentos menores...")
                segmentos = dividir_audio(path_mp3, Path(tmpdir), duracao_segmento=duracao_segmento)
                st.success(f"Áudio dividido em {len(segmentos)} segmentos")

                # Transcrição dos segmentos
                st.info("📝 Transcrevendo segmentos de áudio...")
                texto_transcrito = transcrever_segmentos(segmentos)
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
