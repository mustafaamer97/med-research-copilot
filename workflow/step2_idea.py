import streamlit as st

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

        context = st.session_state.get(
            "research_context",
            {}
        )

        if not context:

            st.warning(
                "Please complete Step 1 first."
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

        if st.button(
            "Generate Ideas"
        ):

            with st.spinner(
                "Generating research ideas..."
            ):

                ideas = generate_research_ideas(
                    research_context=context
                )

            st.session_state[
                "generated_ideas"
            ] = ideas

        if st.session_state.get(
            "generated_ideas"
        ):

            st.subheader(
                "Suggested Research Ideas"
            )

            st.write(
                st.session_state[
                    "generated_ideas"
                ]
            )

            st.caption(
                "Generated using evidence retrieval, research gap analysis, and medical research methodology rules."
            )

            validation = validate_idea_quality(
                context,
                st.session_state["generated_ideas"]
            )

            st.subheader(
                "🔬 Automated Idea Validation"
            )

            st.metric(
                "Feasibility",
                validation["feasibility"]
            )

            st.metric(
                "Novelty",
                validation["novelty"]
            )

            st.metric(
                "Clinical Importance",
                validation["clinical_importance"]
            )

            st.metric(
                "Overall Score",
                validation["overall_score"]
            )

            with st.expander(
                "Validation Explanation"
            ):

                for item in validation["notes"]:
                    st.write(
                        "• " + item
                    )

            if st.button(
                "Select Best Research Idea"
            ):

                st.session_state[
                    "selected_research_idea"
                ] = {

                    "title":
                    st.session_state.get(
                        "generated_title",
                        "AI Generated Research Idea"
                    ),

                    "description":
                    st.session_state[
                        "generated_ideas"
                    ],

                    "source":
                    "AI",

                    "validation":
                    validation,

                    "research_goal":
                    context.get(
                        "research_goal",
                        ""
                    ),

                    "context":
                    context
                }

                st.session_state[
                    "idea_completed"
                ] = True

                st.session_state[
                    "current_step"
                ] = 3

                st.success(
                    "Research idea saved successfully."
                )

    # ==================================
    # Existing Idea
    # ==================================

    else:

        st.info(
            "Describe your research idea in a structured format."
        )

        col1, col2 = st.columns(2)

        with col1:

            disease = st.text_input(
                "Disease / Condition"
            )

            location = st.text_input(
                "Location / Setting"
            )

        with col2:

            outcome = st.text_input(
                "Main Outcome"
            )

            period = st.text_input(
                "Study Period"
            )

        idea_title = st.text_input(
            "Research Idea Title"
        )

        idea_description = st.text_area(
            "Research Idea Description",
            height=150
        )

        research_goal = st.text_input(
            "Research Goal",
            placeholder="Incidence, Risk factors, Treatment outcome..."
        )

        st.markdown("### Research Idea Preview")

        preview = f"""
Disease / Condition:
{disease}

Location:
{location}

Outcome:
{outcome}

Study Period:
{period}

Description:
{idea_description}
"""

        st.info(preview)

        if idea_title and idea_description:

            st.success(
                "Idea structure looks complete."
            )

        else:

            st.warning(
                "Please add title and description."
            )

        manual_validation = validate_manual_idea(
            disease=disease,
            outcome=outcome,
            description=idea_description
        )

        st.subheader(
            "Idea Quality Check"
        )

        st.metric(
            "Overall Score",
            manual_validation["overall_score"]
        )

        with st.expander(
            "Validation Notes"
        ):

            for note in manual_validation["notes"]:
                st.write(
                    "• " + note
                )

        if st.button(
            "Save Research Idea"
        ):

            st.session_state[
                "selected_research_idea"
            ] = {

                "title":
                idea_title,

                "description":
                idea_description,

                "source":
                "manual",

                "disease":
                disease,

                "location":
                location,

                "outcome":
                outcome,

                "period":
                period,

                "validation":
                manual_validation,

                "research_goal":
                research_goal,

                "context":
                st.session_state.get(
                    "research_context",
                    {}
                )
            }

            st.session_state[
                "idea_completed"
            ] = True

            st.session_state[
                "current_step"
            ] = 3

            st.success(
                "Research idea saved successfully."
            )

    # ==================================
    # Completion Status
    # ==================================

    if st.session_state.get(
        "selected_research_idea"
    ):

        st.success(
            "✅ Step 2 Completed"
        )
