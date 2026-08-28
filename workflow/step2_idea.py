import streamlit as st
from modules.idea_generator import generate_research_ideas
from modules.idea_validator import validate_idea_quality, validate_manual_idea

def render():
    st.header("💡 Step 2: Research Idea Generation & Gap Analysis")

    # قراءة الـ Context المخزّن في الخطوة الأولى
    context = st.session_state.get("research_context", {})

    if not context:
        st.warning("Please complete Step 1 first.")
        return

    # =========================
    # التعديل 1: منع توليد أفكار إذا كان Step 1 ضعيفاً
    # =========================
    validation = st.session_state.get("context_validation", {})
    if validation.get("score", 0) < 50:
        st.error("Research context quality is too low. Please improve Step 1 first.")
        return

    # عرض بيانات Step 1 بشكل منظم
    st.subheader("Research Context")
    st.info(
        f"""
**Field:** {context.get('field', '')}  
**Disease/Topic:** {context.get('disease', context.get('research_topic', ''))}  
**Population:** {context.get('population', '')}  
**Outcome:** {context.get('outcome', '')}  
**Goal:** {context.get('research_goal', '')}  
**Design:** {context.get('study_design', context.get('recommended_design', ''))}
"""
    )

    # =========================
    # التعديل 2: عرض منهجية الدراسة القادمة
    # =========================
    st.markdown("### Planned Research Path")
    st.success(
        f"""
Step 1 → Context  
Step 2 → Idea  
Step 3 → Research Question  
Step 4 → Literature Search  
Step 5 → Screening  
Using: {context.get('recommended_design', '')}
"""
    )

    st.divider()

    # =========================
    # التعديل 3 & 4: تحسين زر Generate Ideas و الـ Spinner
    # =========================
    if st.button(
        "Generate Evidence-Based Ideas",
        use_container_width=True,
        type="primary"
    ):
        with st.spinner("Searching evidence and identifying research gaps..."):
            ideas_result = generate_research_ideas(context)
            st.session_state["generated_ideas"] = ideas_result

    # عرض الأفكار والتحليلات الناتجة
    if "generated_ideas" in st.session_state:
        generated = st.session_state["generated_ideas"]
        
        if generated.get("status") == "no_evidence":
            st.warning(generated.get("message"))
        else:
            # =========================
            # التعديل 5 & 6: عرض Gap Score و Research Gaps
            # =========================
            gap_analysis = generated.get("gap_analysis", {})
            if gap_analysis:
                st.subheader("Research Gap Assessment")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Gap Score", gap_analysis.get("gap_score", 0))
                with col2:
                    st.metric("Evidence Studies", gap_analysis.get("total_papers", 0))
                with col3:
                    st.metric("Recent Evidence %", gap_analysis.get("recent_evidence_ratio", 0))

                if gap_analysis.get("research_gaps"):
                    with st.expander("Detected Research Gaps"):
                        for gap in gap_analysis["research_gaps"]:
                            st.write(f"• {gap}")

            st.subheader("Generated Research Ideas")
            st.write(generated.get("ideas"))

            # اختيار وحفظ فكرة مقترحة
            selected_idea_text = st.text_area(
                "Select or Edit your preferred idea text:",
                value=str(generated.get("ideas", "")),
                height=150
            )

            if st.button("Save Selected Idea", type="primary"):
                # =========================
                # التعديل 7 & 8: تحسين حفظ الفكرة وربطها بـ Step 3
                # =========================
                st.session_state["selected_research_idea"] = {
                    "description": selected_idea_text,
                    "topic": context.get("disease", ""),
                    "population": context.get("population", ""),
                    "outcome": context.get("outcome", ""),
                    "recommended_design": context.get("recommended_design", ""),
                    "data_source": context.get("data_source", "")
                }
                st.session_state["idea_completed"] = True
                st.session_state["current_step"] = 3
                st.info("Next Step: Build a structured research question.")
                st.success("Research idea saved successfully!")

    st.divider()

    # قسم الإدخال اليدوي للفكرة
    st.subheader("Or Enter Your Own Research Idea")

    # =========================
    # التعديل 9: تحسين Manual Idea Validation
    # =========================
    if context:
        st.info(
            f"""
Recommended Design: {context.get('recommended_design', '')}  
Recommended Population: {context.get('population', '')}
"""
        )

    manual_idea = st.text_area("Your Custom Research Idea", height=100)

    if st.button("Validate & Save Custom Idea"):
        if manual_idea.strip():
            manual_validation = validate_manual_idea(manual_idea, context)
            
            # =========================
            # التعديل 7 & 8 للمدخل اليدوي
            # =========================
            st.session_state["selected_research_idea"] = {
                "description": manual_idea,
                "validation": manual_validation,
                "topic": context.get("disease", ""),
                "population": context.get("population", ""),
                "outcome": context.get("outcome", ""),
                "recommended_design": context.get("recommended_design", ""),
                "data_source": context.get("data_source", "")
            }
            st.session_state["idea_completed"] = True
            st.session_state["current_step"] = 3
            st.info("Next Step: Build a structured research question.")
            st.success("Custom research idea validated and saved!")

    # =========================
    # التعديل 10: زر الانتقال المباشر إلى Step 3
    # =========================
    if st.session_state.get("idea_completed"):
        st.success("✅ Step 2 Completed")
        if st.button("➡ Continue to Step 3", use_container_width=True):
            st.session_state["current_step"] = 3
            st.rerun()
