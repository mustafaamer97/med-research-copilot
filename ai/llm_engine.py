import os
import streamlit as st

# دعم استيراد المكتبة المتوفرة في البيئة (google-genai أو google-generativeai)
try:
    import google.generativeai as genai
    USING_NEW_SDK = False
except ImportError:
    from google import genai
    USING_NEW_SDK = True


def get_api_key():
    """جلب المفتاح آلياً من Streamlit Secrets أو المتغيرات المحلية."""
    return st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")


def list_available_models():

    models = []

    for model in genai.list_models():

        models.append(
            model.name
        )

    return models


def ask_ai(prompt: str, model_name: str = "gemini-1.5-flash") -> str:
    """إرسال الاستعلام واستلام الرد مع التكفل بالمعالجة والاستثناءات."""
    api_key = get_api_key()
    if not api_key:
        return "AI Error: لم يتم إعداد GEMINI_API_KEY داخل Streamlit Secrets."

    try:
        if not USING_NEW_SDK:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        else:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
    except Exception as e:
        # إذا تعذر النموذج الأول، يتم تجربة gemini-1.5-pro كخيار احتياطي
        if "404" in str(e) and model_name != "gemini-1.5-pro":
            return ask_ai(prompt, model_name="gemini-1.5-pro")
        return f"AI Error: {str(e)}"
