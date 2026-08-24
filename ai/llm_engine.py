import os
import streamlit as st
import google.generativeai as genai
from ai.system_prompt import SYSTEM_PROMPT
from ai.ai_guardrails import validate_prompt

# جلب API Key آلياً سواء من Streamlit Secrets أو من المتغيرات المحلية
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ضبط أسماء النماذج وفقاً لطلبك
PRIMARY_MODEL = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-3.5-flash"


def ask_ai(prompt: str) -> str:
    """
    إرسال الاستعلام إلى نموذج Gemini بعد التحقق من قواعد الحماية (Guardrails) 
    مع إرفاق SYSTEM_PROMPT والتعامل مع الأخطاء والتحويل التلقائي للنموذج الاحتياطي.
    """
    if not api_key:
        return "AI Error: لم يتم إعداد GEMINI_API_KEY داخل Secrets في Streamlit Cloud."

    # التحقق من سلامة النص المدخل عبر AI Guardrails قبل إرسال الطلب
    if not validate_prompt(prompt):
        return "Request blocked by AI Guardrails."

    try:
        model = genai.GenerativeModel(
            PRIMARY_MODEL,
            system_instruction=SYSTEM_PROMPT
        )
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # تجربة النموذج الاحتياطي في حال حدوث خلل مؤقت أو خطأ 404
        try:
            fallback_model = genai.GenerativeModel(
                FALLBACK_MODEL,
                system_instruction=SYSTEM_PROMPT
            )
            response = fallback_model.generate_content(prompt)
            return response.text
        except Exception as fallback_error:
            return f"AI Error: {str(e)} | Fallback Error: {str(fallback_error)}"
