import streamlit as st
from modules.build_pico import build_pico

def render():
    st.header("❓ Research Question Builder")

    # قراءة الـ Context المخزّن في الخطوة الأولى
    context = st.session_state.get("research_context", {})

    if not context:
        st.warning("Please complete Step 1 first.")
        return

    # عرض بيانات Step 1 بشكل منظم
    st.subheader("Research Context")
    st.info(
        f"""
**Field:** {context.get('field', '')}  
**Disease:** {context.get('disease', '')}  
**Population:** {context.get('population', '')}  
**Outcome:** {context.get('outcome', '')}  
**Goal:** {context.get('research_goal', '')}  
**Design:** {context.get('study_design', '')}
"""
    )

    # استدعاء عناصر PICO/PECO/PEO من الـ Context
    population = context.get("population", "")
    intervention = context.get("intervention", context.get("exposure", ""))
    comparison = context.get("comparison", "")
    outcome = context.get("outcome", "")
    
    # ---------------------------------------------------------
    # الفلتر والقيد الإلزامي لنوع التصميم المختار (Study Design Constraint)
    # ---------------------------------------------------------
    selected_design = context.get("study_design", "")

    # توليد سؤال البحث عبر وحدة build_pico مع تمرير التصميم المكتشف كقيد إلزامي
    question_data = build_pico(
        population=population,
        intervention=intervention,
        comparison=comparison,
        outcome=outcome,
        study_design=selected_design,
        research_goal=context.get("research_goal", "")
    )

    # عرض سؤال البحث المولد والكلمات المفتاحية
    st.subheader("Generated Research Question")
    st.success(question_data["question"])

    st.subheader("Search Keywords")
    st.code(question_data["keywords"])

    # إمكانية تعديل السؤال يدوياً
    edited_question = st.text_area(
        "Edit Research Question",
        value=question_data["question"],
        height=120
    )

    # حفظ سؤال البحث للانتقال للخطوة التالية
    if st.button("Save Research Question", type="primary", use_container_width=True):
        st.session_state["research_question"] = {
            "question": edited_question,
            "keywords": question_data["keywords"],
            "pico": question_data.get("pico", {}),
            "research_goal": context.get("research_goal", ""),
            "study_design": selected_design
        }

        st.session_state["question_completed"] = True
        st.session_state["current_step"] = 3

        st.success("Research question saved successfully.")

    # عرض حالة الإكمال عند الحفظ
    if st.session_state.get("research_question"):
        st.success("✅ Step 2 Completed")
        with st.expander("Saved Research Question Details", expanded=True):
            saved = st.session_state["research_question"]
            st.markdown(f"**Question:** {saved.get('question')}")
            st.markdown(f"**Target Design:** {saved.get('study_design')}")
            st.markdown(f"**Keywords:** `{saved.get('keywords')}`")
