import os
import streamlit as st
import google.generativeai as genai
from ai.system_prompt import SYSTEM_PROMPT
from ai.ai_guardrails import validate_prompt, validate_response

# جلب API Key آلياً سواء من Streamlit Secrets أو من المتغيرات المحلية
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ضبط أسماء النماذج
PRIMARY_MODEL = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-3.5-flash"


def ask_ai(prompt: str, user_input: str = "") -> str:
    """
    إرسال الطلب إلى Gemini مع تطبيق Guardrails
    على مدخل المستخدم وفحص الرد علمياً لمنع الهلوسة.
    """

    if not api_key:
        return (
            "AI Error: GEMINI_API_KEY not configured."
        )

    # فحص مدخل المستخدم فقط
    if user_input:

        if not validate_prompt(user_input):

            return (
                "Request blocked by AI Guardrails."
            )

    try:

        model = genai.GenerativeModel(
            PRIMARY_MODEL,
            system_instruction=SYSTEM_PROMPT
        )

        response = model.generate_content(
            prompt
        )

        response_text = response.text

        if not validate_response(response_text):
            return (
                "AI Safety Error: "
                "Response failed scientific validation."
            )

        return response_text

    except Exception as e:

        try:

            fallback_model = genai.GenerativeModel(
                FALLBACK_MODEL,
                system_instruction=SYSTEM_PROMPT
            )

            response = fallback_model.generate_content(
                prompt
            )

            response_text = response.text

            if not validate_response(response_text):
                return (
                    "AI Safety Error: "
                    "Response failed scientific validation."
                )

            return response_text

        except Exception as fallback_error:

            return (
                f"AI Error: {str(e)} | "
                f"Fallback Error: {str(fallback_error)}"
            )
