import os
import streamlit as st
import google.generativeai as genai
from ai.system_prompt import SYSTEM_PROMPT
from ai.ai_guardrails import validate_prompt, validate_response

# جلب API Key آلياً سواء من Streamlit Secrets أو من المتغيرات المحلية
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ضبط أسماء النماذج بمرونة عبر المتغيرات البيئية مع قيم افتراضية
PRIMARY_MODEL = os.getenv(
    "PRIMARY_GEMINI_MODEL",
    "gemini-3.6-flash"
)
FALLBACK_MODEL = os.getenv(
    "FALLBACK_GEMINI_MODEL",
    "gemini-3.5-flash"
)

# إعدادات التوليد لتقليل العشوائية وضمان الدقة في الأبحاث الطبية
GENERATION_CONFIG = {
    "temperature": 0.2,
    "top_p": 0.9,
    "max_output_tokens": 8192,
}

# الحد الأقصى لطول الـ Prompt لمنع تجاوز الحدود أو الأخطاء
MAX_PROMPT_LENGTH = 50000


def ask_ai(prompt: str, user_input: str = "") -> str:
    """
    إرسال الطلب إلى Gemini مع تطبيق Guardrails على مدخل المستخدم،
    فحص طول الـ Prompt، معالجة الردود الفارغة، وفحص الرد علمياً لمنع الهلوسة.
    """

    if not api_key:
        return "AI Error: GEMINI_API_KEY not configured."

    # فحص طول الـ Prompt
    if len(prompt) > MAX_PROMPT_LENGTH:
        return "AI Error: Prompt too large."

    # فحص مدخل المستخدم فقط
    if user_input:
        if not validate_prompt(user_input):
            return "Request blocked by AI Guardrails."

    try:
        model = genai.GenerativeModel(
            PRIMARY_MODEL,
            system_instruction=SYSTEM_PROMPT
        )

        response = model.generate_content(
            prompt,
            generation_config=GENERATION_CONFIG
        )

        response_text = getattr(
            response,
            "text",
            ""
        )
        if not response_text:
            return "AI Error: Empty response returned."

        if not validate_response(response_text):
            return (
                "AI Safety Error: "
                "Response failed scientific validation."
            )

        return response_text

    except Exception as e:
        primary_error = e

        try:
            fallback_model = genai.GenerativeModel(
                FALLBACK_MODEL,
                system_instruction=SYSTEM_PROMPT
            )

            response = fallback_model.generate_content(
                prompt,
                generation_config=GENERATION_CONFIG
            )

            response_text = getattr(
                response,
                "text",
                ""
            )
            if not response_text:
                return "AI Error: Empty response returned."

            if not validate_response(response_text):
                return (
                    "AI Safety Error: "
                    "Response failed scientific validation."
                )

            return response_text

        except Exception as fallback_error:
            # عرض التفاصيل التقنية للتشخيص في الواجهة دون إزعاج المستخدم برسائل معقدة
            st.error(f"Primary Error: {primary_error}")
            st.error(f"Fallback Error: {fallback_error}")

            return "AI Error: Unable to generate content at this time."
