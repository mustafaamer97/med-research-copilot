import os
import streamlit as st
import google.generativeai as genai

# جلب API Key آلياً سواء من Streamlit Secrets أو من المتغيرات المحلية
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

SYSTEM_PROMPT = """
You are an evidence-based medical research assistant.

Rules:
- Never invent references.
- Never invent DOI numbers.
- Never invent PMID numbers.
- Never invent statistical results.
- Never invent clinical guideline recommendations.
- If evidence is unavailable, say so.
- Distinguish facts from assumptions.
- Prioritize scientific accuracy over completeness.
"""

# ضبط النموذج الأساسي ليكون الموديل المتاح والمنصوح به
PRIMARY_MODEL = "models/gemini-1.5-flash"
FALLBACK_MODEL = "models/gemini-1.5-pro"

def ask_ai(prompt: str) -> str:
    """
    إرسال الاستعلام إلى نموذج Gemini مع إضافة SYSTEM_PROMPT 
    والتعامل مع الأخطاء والتحويل التلقائي للنموذج الاحتياطي.
    """
    if not api_key:
        return "AI Error: لم يتم إعداد GEMINI_API_KEY داخل Secrets في Streamlit Cloud."

    # دمج تعليمات النظام العامة مع الاستعلام المدخل
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser Request:\n{prompt}"

    try:
        model = genai.GenerativeModel(PRIMARY_MODEL)
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        # تجربة النموذج الاحتياطي في حال حدوث خلل مؤقت أو خطأ في النموذج الأساسي
        try:
            fallback_model = genai.GenerativeModel(FALLBACK_MODEL)
            response = fallback_model.generate_content(full_prompt)
            return response.text
        except Exception as fallback_error:
            return f"AI Error: {str(e)} | Fallback Error: {str(fallback_error)}"
