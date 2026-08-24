import os
import streamlit as st
import google.generativeai as genai
from ai.system_prompt import SYSTEM_PROMPT

# جلب API Key آلياً سواء من Streamlit Secrets أو من المتغيرات المحلية
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ضبط النموذج الأساسي والنموذج الاحتياطي
PRIMARY_MODEL = "gemini-1.5-flash"
FALLBACK_MODEL = "gemini-1.5-pro"


def ask_ai(prompt: str) -> str:
    """
    إرسال الاستعلام إلى نموذج Gemini مع إضافة SYSTEM_PROMPT كتعليمات نظام
    والتعامل مع الأخطاء والتحويل التلقائي للنموذج الاحتياطي.
    """
    if not api_key:
        return "AI Error: لم يتم إعداد GEMINI_API_KEY داخل Secrets في Streamlit Cloud."

    # تجهيز نظام الرسائل واستخدام SYSTEM_PROMPT المستورد
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        # استخدام system_instruction لضمان التزام النموذج بقواعد النظام
        model = genai.GenerativeModel(
            PRIMARY_MODEL,
            system_instruction=SYSTEM_PROMPT
        )
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # تجربة النموذج الاحتياطي في حال حدوث خلل مؤقت
        try:
            fallback_model = genai.GenerativeModel(
                FALLBACK_MODEL,
                system_instruction=SYSTEM_PROMPT
            )
            response = fallback_model.generate_content(prompt)
            return response.text
        except Exception as fallback_error:
            return f"AI Error: {str(e)} | Fallback Error: {str(fallback_error)}"
