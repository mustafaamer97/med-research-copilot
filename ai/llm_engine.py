import os
import streamlit as st
import google.generativeai as genai

# جلب المفتاح آلياً من Streamlit Secrets أو من المتغيرات المحلية (Environment Variables)
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# تحديث اسم النموذج إلى الإصدار الحديث والموصى به
model = genai.GenerativeModel("gemini-1.5-flash")


def ask_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"
