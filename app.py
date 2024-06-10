import streamlit as st
import google.generativeai as genai
import os

st.header("Uygulama")

genai.configure(api_key="AIzaSyBjnu3n-XSsCe1UtEFMZ4Obhd4HY12FaH4")

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
            "temperature": 0.9,
            "top_p": 0.30,
            "top_k": 64,
            "max_output_tokens": 18192,
            "response_mime_type": "text/plain",
        }


    model = genai.GenerativeModel(
        safety_settings = safety_settings,
        generation_config = generation_config,
        model_name ="gemini-1.5-flash-latest")

    response = model.generate_content(prompt).text

    return response

prompt = st.text_input("Lütfen sorgunuzu belirtiniz:")


if st.button("Üret"):

    response = get_gemini_response(prompt)
    st.markdown(response)

