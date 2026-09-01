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
    validate_idea_quality,
    validate_manual_idea
)


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

    # ==================================
    # Generate New Idea
    # ==================================

    if idea_mode == "Generate New Research Idea":

        context = get_context()

        if not context:
            st.warning(
                "Please complete Step 1 first."
            )
            return

        # 3. الاعتماد على is_completed بدلاً من session_state
        if not is_completed("context"):
            st.warning(
                "Please complete and save Step 1 first."
            )
            return

        st.info(
            f"""
Field:
{context.get('field','')}

Topic:
{context.get('disease','')}

Goal:
{context.get('research_goal','')}

Population:
{context.get('population','')}

Recommended Design:
{context.get('recommended_design','')}

Data Source:
{context.get('data_source','')}

Location:
{context.get('location','')}
"""
        )

        if st.button("Generate Ideas"):
            with st.spinner("Generating research ideas..."):
                ideas_result = generate_research_ideas(
                    research_context=context
                )

            if ideas_result.get("status") != "success":
                st.error(
                    ideas_result.get(
                        "message",
                        "Unable to generate ideas."
                    )
                )
                return

            st.session_state["generated_ideas"] = ideas_result.get("ideas", [])

        # 4. إعادة بناء التصميم لعرض الأفكار كقائمة تفاعلية
        generated_ideas_list = st.session_state.get("generated_ideas", [])

        if generated_ideas_list:
            st.subheader("Suggested Research Ideas")

            for index, idea in enumerate(generated_ideas_list, start=1):
                idea_title = idea.get("title", f"Research Idea {index}")
                
                with st.expander(f"💡 Idea {index}: {idea_title}", expanded=(index == 1)):
                    st.markdown(f"**Research Question:** {idea.get('research_question', 'N/A')}")
                    st.markdown(f"**Research Gap:** {idea.get('gap', 'N/A')}")
                    st.markdown(f"**Clinical Impact:** {idea.get('impact', 'N/A')}")
                    st.markdown(f"**Rationale:** {idea.get('rationale', 'N/A')}")

                    # إجراء تقييم آلي للفكرة الفردية بناءً على الـ context
                    validation = validate_idea_quality(context)

                    st.markdown("---")
                    st.markdown("##### 🔬 Automated Idea Validation")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Feasibility", validation.get("feasibility", "-"))
                    col2.metric("Novelty", validation.get("novelty", "-"))
                    col3.metric("Clinical Importance", validation.get("clinical_importance", "-"))
                    col4.metric("Overall Score", validation.get("overall_score", "-"))

                    if st.button(f"Select Idea {index}", key=f"select_idea_{index}"):
                        selected_idea = {
                            "title": idea_title,
                            "rationale": idea.get("rationale", ""),
                            "research_question": idea.get("research_question", ""),
                            "gap": idea.get("gap", ""),
                            "impact": idea.get("impact", ""),
                            "source": "AI",
                            "validation": validation,
                            "research_goal": context.get("research_goal", ""),
                            "disease": context.get("disease", ""),
                            "population": context.get("population", ""),
                            "outcome": context.get("outcome", ""),
                            "study_design": context.get("recommended_design", context.get("study_design", "")),
                            "data_source": context.get("data_source", ""),
                            "field": context.get("field", ""),
                            "location": context.get("location", ""),
                            "study_period": context.get("study_period", "")
                        }

                        # 2. تحديث التخزين عبر Context Manager وحذف Session State الزائد
                        update_context(
                            selected_research_idea=selected_idea,
                            idea_title=selected_idea.get("title", ""),
                            idea_rationale=selected_idea.get("rationale", "")
                        )
                        
                        mark_completed("idea")
                        st.success("Research idea saved successfully.")

    # ==================================
    # Existing Idea (Manual)
    # ==================================

    else:

        context = get_context()

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

        manual_validation = validate_manual_idea(
            disease=disease,
            outcome=outcome,
            description=idea_description
        )

        st.subheader("Idea Quality Check")
        st.metric("Overall Score", manual_validation.get("overall_score", "-"))

        with st.expander("Validation Notes"):
            for note in manual_validation.get("notes", []):
                st.write("• " + note)

        if idea_title and idea_description and disease:
            if st.button("Save Research Idea"):
                selected_idea = {
                    "title": idea_title,
                    "rationale": idea_description,
                    "source": "manual",
                    "disease": disease,
                    "location": location,
                    "primary_outcome": outcome,
                    "period": period,
                    "validation": manual_validation,
                    "research_goal": research_goal,
                    # 3. الاعتماد على context مباشرة
                    "population": context.get("population", ""),
                    "study_design": context.get("recommended_design", context.get("study_design", "")),
                    "data_source": context.get("data_source", ""),
                    "field": context.get("field", ""),
                }

                # 2 & 3. التحديث الحصري عبر Context Manager واستدعاء mark_completed
                update_context(
                    selected_research_idea=selected_idea,
                    idea_title=selected_idea.get("title", ""),
                    idea_rationale=selected_idea.get("rationale", "")
                )

                mark_completed("idea")
                st.success("Research idea saved successfully.")

    # ==================================
    # Completion Status
    # ==================================

    if is_completed("idea") or get_context().get("selected_research_idea"):
        st.success("✅ Step 2 Completed")
