import streamlit as st

from modules.idea_generator import (
    generate_research_ideas
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
                    context
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
                "Generated from PubMed / Europe PMC / OpenAlex evidence and research gap analysis."
            )

            st.subheader(
                "🔬 Idea Validation"
            )

            validation_score = st.slider(
                "Feasibility Score",
                0,
                100,
                70
            )

            novelty_score = st.slider(
                "Novelty Score",
                0,
                100,
                70
            )

            clinical_score = st.slider(
                "Clinical Importance",
                0,
                100,
                70
            )

            overall_score = int(
                (
                    validation_score
                    +
                    novelty_score
                    +
                    clinical_score
                )
                /
                3
            )

            st.success(
                f"""
Overall Research Idea Score:
{overall_score}/100
"""
            )

            if st.button(
                "Use Generated Ideas"
            ):

                st.session_state[
                    "selected_research_idea"
                ] = {

                    "title":
                    "Generated Research Idea",

                    "description":
                    st.session_state[
                        "generated_ideas"
                    ],

                    "source":
                    "AI",

                    "validation": {

                        "feasibility":
                        validation_score,

                        "novelty":
                        novelty_score,

                        "clinical_importance":
                        clinical_score,

                        "overall":
                        overall_score
                    },

                    "context":
                    context
                }

                st.session_state[
                    "idea_completed"
                ] = True

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
                period
            }

            st.session_state[
                "idea_completed"
            ] = True

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
