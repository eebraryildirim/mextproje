import os
import io
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from PyPDF2 import PdfReader
import fitz  # this is pymupdf


st.set_page_config(page_title="ATS Sistemi",
                   page_icon=":robot:",
                   initial_sidebar_state="expanded")

st.header("Uygulama v1")

genai.configure(api_key= "AIzaSyAmXC386mweCOOW6NgF496s24I1GMNGifQ")


@st.cache_resource
def read_pdf(file):
    pdfReader = PdfReader(file)
    count = len(pdfReader.pages)

    all_page_text = ""

    for i in range(count):  # for i in range (0, count-1) ///  for i in range (len(pdfReader.pages))
        page = pdfReader.pages[i]
        all_page_text += page.extract_text()

    return all_page_text


@st.cache_resource
def read_pdf_2(file_path):
    doc = fitz.open(file_path)
    images = []
    # count = len(doc)
    for i in range(len(doc)):  # for i in range(count)
        page = doc.load_page(i)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

@st.cache_resource
def get_gemini_response(prompt):
    safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_LOW_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]


    generation_config = {
            "temperature": 0.4,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 18192,
            "response_mime_type": "text/plain",
        }


    model = genai.GenerativeModel(
        safety_settings = safety_settings,
        generation_config = generation_config,
        model_name ="gemini-1.5-flash-latest")

    prompt_token_count = model.count_tokens(prompt)

    response = model.generate_content(prompt).text

    response_token_count = model.count_token(response)

    total_token_count = model.count_token(response)
    total_token_count = int(total_token_count)

    return response, total_token_count





st.sidebar.header("ATS v2 Hoşgeldiniz")

deneyim_suresi = st.number_input(label = "Deneyim süresi", min_value=0,max_value = 15, value=2)


#st.file

user_input  = st.text_input("lütfen sorgunuzu beliritniz:")

prompt = (f"""
Sen 10 yıllık tecrübeli bir İk uzmanısın.Eline gelen CV örenğindeki iş ilanı için minimum 5 yıl deneyimli aday aranıyor. Gönderilen CV örneğindeki adayın tecrübe süresi {deneyim_suresi} yıldır.
         """)

st.sidebar.radio("Döküman uzantınızı seçin", ["PDF", "PDF uzantılı olmayan"])

if st.button("Üret"):

    response = get_gemini_response(prompt)
    st.markdown(response)

