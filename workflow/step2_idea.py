import streamlit as st

from modules.context_manager import (
    get_context,
    update_context,
    is_completed,
    mark_completed
)
from modules.idea_generator import (
    generate_research_ideas
)
from modules.idea_validator import (
    validate_manual_idea
)


def save_selected_idea(selected_idea: dict):
    """
    دالة موحدة لحفظ الفكرة المختارة داخل Context Manager 
    وتحديث مخرجاتها مع حفظ Objectives و PICO وتحديث مفاتيح P, I, C, O لـ Step 3.
    """
    # [التعديل 2]: إضافة objectives و pico داخل context_updates
    context_updates = {
        "selected_research_idea": selected_idea,
        "idea_title": selected_idea.get("title", ""),
        "idea_rationale": selected_idea.get("rationale", ""),
        "research_question": selected_idea.get("research_question", ""),
        "objectives": selected_idea.get("objectives", []),
        "pico": selected_idea.get("pico", {})
    }

    # [التعديل 1]: إصلاح مفاتيح PICO للربط مع مفاتيح الـ P, I, C, O الصحيحة
    pico = selected_idea.get("pico", {})
    if pico:
        context_updates.update({
            "population": pico.get("P", get_context().get("population", "")),
            "exposure_or_intervention": pico.get("I", ""),
            "comparison": pico.get("C", ""),
            "primary_outcome": pico.get("O", get_context().get("outcome", ""))
        })

    update_context(**context_updates)
    mark_completed("idea")


def render():

    st.header(
        "💡 Idea Generator & Validation"
    )

    idea_mode = st.radio(
        "Research Idea Source",
        [
            "Generate New Research Idea",
            "I Already Have a Research Idea"
        ]
    )

    context = get_context()

    # ==================================
    # Generate New Idea
    # ==================================

    if idea_mode == "Generate New Research Idea":

        if not context:
            st.warning("Please complete Step 1 first.")
            return

        if not is_completed("context"):
            st.warning("Please complete and save Step 1 first.")
            return

        st.info(
            f"""
Field: {context.get('field', '')}
Topic: {context.get('disease', '')}
Goal: {context.get('research_goal', '')}
Population: {context.get('population', '')}
Recommended Design: {context.get('recommended_design', '')}
Data Source: {context.get('data_source', '')}
Location: {context.get('location', '')}
"""
        )

        if st.button("Generate Ideas"):
            with st.spinner("Generating research ideas..."):
                ideas_result = generate_research_ideas(
                    research_context=context
                )

            if ideas_result.get("status") != "success":
                st.error(
                    ideas_result.get("message", "Unable to generate ideas.")
                )
                return

            update_context(
                generated_ideas=ideas_result.get("top_ideas", [])
            )
            context = get_context()

        generated_ideas_list = context.get("generated_ideas", [])

        if generated_ideas_list:
            st.subheader("Suggested Research Ideas")

            for index, idea in enumerate(generated_ideas_list, start=1):
                idea_title = idea.get("title", f"Research Idea {index}")
                
                with st.expander(f"💡 Idea {index}: {idea_title}", expanded=(index == 1)):
                    st.markdown(f"**Research Question:** {idea.get('research_question', 'N/A')}")
                    st.markdown(f"**Research Gap:** {idea.get('research_gap', 'N/A')}")
                    st.markdown(f"**Clinical Impact:** {idea.get('impact', 'N/A')}")
                    st.markdown(f"**Rationale:** {idea.get('rationale', 'N/A')}")

                    objectives = idea.get("objectives", [])
                    if objectives:
                        st.markdown("**Objectives:**")
                        for obj in objectives:
                            st.markdown(f"- {obj}")

                    scores = idea.get("scores", {})
                    st.markdown("---")
                    st.markdown("##### 🔬 Automated Idea Validation")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Novelty", scores.get("novelty", "-"))
                    col2.metric("Feasibility", scores.get("feasibility", "-"))
                    col3.metric("Clinical", scores.get("clinical_importance", "-"))
                    col4.metric("Overall", scores.get("overall", "-"))

                    if st.button(f"Select Idea {index}", key=f"select_idea_{index}"):
                        selected_idea = {
                            **idea,
                            "source": "AI",
                            "disease": context.get("disease", ""),
                            "field": context.get("field", ""),
                            "study_design": context.get("recommended_design", context.get("study_design", "")),
                            "data_source": context.get("data_source", ""),
                            "location": context.get("location", ""),
                            "study_period": context.get("study_period", "")
                        }

                        save_selected_idea(selected_idea)
                        # [التعديل 5]: إضافة الاحتفال بتحسين تجربة المستخدم
                        st.balloons()
                        st.success("Research idea saved successfully.")

    # ==================================
    # Existing Idea (Manual)
    # ==================================

    else:

        st.info("Describe your research idea in a structured format.")

        col1, col2 = st.columns(2)

        with col1:
            disease = st.text_input("Disease / Condition", value=context.get("disease", ""))
            location = st.text_input("Location / Setting", value=context.get("location", ""))

        with col2:
            outcome = st.text_input("Main Outcome", value=context.get("outcome", ""))
            period = st.text_input("Study Period", value=context.get("study_period", ""))

        idea_title = st.text_input("Research Idea Title")
        idea_description = st.text_area("Research Idea Description", height=150)
        research_goal = st.text_input(
            "Research Goal",
            value=context.get("research_goal", ""),
            placeholder="Incidence, Risk factors, Treatment outcome..."
        )

        st.markdown("### Research Idea Preview")
        preview = f"""
Disease / Condition: {disease}
Location: {location}
Outcome: {outcome}
Study Period: {period}

Description:
{idea_description}
"""
        st.info(preview)

        if idea_title and idea_description:
            st.success("Idea structure looks complete.")
        else:
            st.warning("Please add title and description.")

        # [التعديل 3]: تعديل استدعاء validate_manual_idea لتمرير description و context
        manual_validation = validate_manual_idea(
            description=idea_description,
            context=context
        )

        st.subheader("Idea Quality Check")
        st.metric("Overall Score", manual_validation.get("overall_score", "-"))

        with st.expander("Validation Notes"):
            for note in manual_validation.get("notes", []):
                st.write("• " + note)

        if idea_title and idea_description and disease:
            if st.button("Save Research Idea"):
                # [التعديل 4]: إدراج objectives و pico في الفكرة اليدوية
                selected_idea = {
                    "title": idea_title,
                    "rationale": idea_description,
                    "research_question": f"What is the {research_goal or 'association'} regarding {disease} in terms of {outcome}?",
                    "source": "manual",
                    "disease": disease,
                    "location": location,
                    "primary_outcome": outcome,
                    "period": period,
                    "validation": manual_validation,
                    "research_goal": research_goal,
                    "population": context.get("population", ""),
                    "study_design": context.get("recommended_design", context.get("study_design", "")),
                    "data_source": context.get("data_source", ""),
                    "field": context.get("field", ""),
                    "objectives": [],
                    "pico": {}
                }

                save_selected_idea(selected_idea)
                # [التعديل 5]: إضافة الاحتفال تحسين تجربة المستخدم
                st.balloons()
                st.success("Research idea saved successfully.")

    # ==================================
    # Completion Status
    # ==================================

    if is_completed("idea"):
        st.success("✅ Step 2 Completed")
