import os
import streamlit as st
import google.generativeai as genai

# جلب API Key آلياً سواء من Streamlit Secrets أو من المتغيرات المحلية
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ضبط النموذج الأساسي ليكون الموديل المتاح والمنصوح به
PRIMARY_MODEL = "models/gemini-3.6-flash"
FALLBACK_MODEL = "models/gemini-flash-latest"

model = genai.GenerativeModel(PRIMARY_MODEL)

def ask_ai(prompt: str) -> str:
    """
    إرسال الاستعلام إلى نموذج Gemini مع التعامل مع الأخطاء والتحويل التلقائي للنموذج الاحتياطي.
    """
    if not api_key:
        return "AI Error: لم يتم إعداد GEMINI_API_KEY داخل Secrets في Streamlit Cloud."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # تجربة النموذج الاحتياطي في حال حدوث خلل مؤقت في الاستدعاء
        try:
            fallback_model = genai.GenerativeModel(FALLBACK_MODEL)
            response = fallback_model.generate_content(prompt)
            return response.text
        except Exception as fallback_error:
            return f"AI Error: {str(e)} | Fallback Error: {str(fallback_error)}"
