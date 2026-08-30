import streamlit as st
from modules.context_manager import get_context
from pages.analytics_page import render as analytics_render


def render():
    context = get_context()

    # Guard clause to ensure Step 8 is completed before proceeding
    if not context.get("data_collection_completed"):
        st.warning(
            "⚠️ Please complete Step 8 (Data Collection Plan) before accessing statistical analytics."
        )
        return

    analytics_render()
