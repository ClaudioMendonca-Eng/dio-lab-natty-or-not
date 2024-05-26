import streamlit as st
from st_functions import st_button, load_css
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

st.write("[![Star](https://img.shields.io/github/stars/ClaudioMendonca-Eng/dio-lab-natty-or-not.svg?logo=github&style=social)](https://gitHub.com/ClaudioMendonca-Eng/dio-lab-natty-or-not)")

load_css()

bar = st.sidebar
bar.markdown("[![Bootcamp Nexa - Fundamentos de IA Generativa e Claude 3](https://raw.githubusercontent.com/ClaudioMendonca-Eng/dio-lab-natty-or-not/main/img/logo_nexa_dio.png)](https://dio.me)")
#bar.image('img/logo_nexa_dio.png', width=250)
bar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Gemini_language_model_logo.png/200px-Gemini_language_model_logo.png', width=200)
bar.title("🔑 Chaves de API")
bar.markdown("Para usar este aplicativo, você precisa de uma chave de API do Gemini. Você pode obter uma chave de API do Gemini [aqui](https://aistudio.google.com/app/apikey).")
api_key = bar.text_input("Digite sua API Key do Gemini:", type="password")
# Configuração da API Key do Gemini
genai.configure(api_key=api_key)

# Configurações de segurança para o modelo Gemini Pro
#"Bloquear nenhum": "BLOCK_NONE",
#"Bloquear poucos": "BLOCK_ONLY_HIGH",
#"Bloquear alguns": "BLOCK_MEDIUM_AND_ABOVE",
#"Bloquear muitos": "BLOCK_LOW_AND_ABOVE"

safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]

#Altere o prompt de acordo com o seu uso.
prompt="""
        Título: Notas Detalhadas da Transcrição do Vídeo do YouTube

        Como especialista em vídeos do YouTube, sua tarefa é fornecer notas detalhadas com base na transcrição de um vídeo do YouTube que eu fornecerei. Assuma o papel de um estudante e gere notas abrangentes cobrindo os principais conceitos discutidos no vídeo.

        Suas notas devem:
        - Ser detalhadas e abrangentes.
        - Cobrir os principais conceitos discutidos no vídeo.
        - Destacar os pontos principais e os principais aprendizados do vídeo.
        - Explicar todos os detalhes do vídeo.

        Por favor, forneça a transcrição do vídeo do YouTube, e eu gerarei as notas detalhadas do vídeo do YouTube conforme necessário.
        """


## obtendo os dados de transcrição de vídeos do YouTube.
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]

        # Use esta linha se você quiser obter vídeos do YouTube apenas em inglês.
        # transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        # Esta parte converte qualquer vídeo com transcrição em qualquer idioma para uma transcrição em portugues-br.
        transcript_list=YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            transcript_text=transcript.fetch()
            transcript_text=transcript.translate('pt').fetch()

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## Obtendo o resumo com base no Prompt do Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text
        
st.title("🎥 𝚈𝚘𝚞𝚝𝚞𝚋𝚎 Notas Detalhadas 📝")
st.info("Converta vídeos do YouTube com transcrição para notas detalhadas em inglês usando o Conversor Gemini Pro. Funciona com qualquer idioma e traduz automaticamente. Basta inserir o link e clicar!")
youtube_link = st.text_input("Insira o link do vídeo do YouTube:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)


if st.button("Obtenha notas do vídeo"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
icon_size = 20
st_button('site', 'https://claudiomendonca.eng.br', '    Explore meu portfólio visitando o meu site', icon_size)
st_button('linkedin', 'https://www.linkedin.com/in/claudio-mendonca', '    Conecte-se comigo no LinkedIn', icon_size)
st_button('github', 'https://github.com/ClaudioMendonca-Eng', '    Confira meu perfil no Github', icon_size)
