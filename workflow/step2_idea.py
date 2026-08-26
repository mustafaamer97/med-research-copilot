import streamlit as st

from modules.idea_generator import (
    generate_research_ideas
)


def render():

    st.header(
        "💡 Research Idea Workspace"
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

        field = context.get(
            "field",
            ""
        )

        st.info(
            f"""
Field: {context.get('field','')}

Population: {context.get('population','')}

Study Design: {context.get('study_design','')}

Data Source: {context.get('data_source','')}
"""
        )

        if st.button(
            "Generate Ideas"
        ):

            if field:

                with st.spinner(
                    "Generating research ideas..."
                ):

                    ideas = generate_research_ideas(
                        field
                    )

                st.session_state[
                    "generated_ideas"
                ] = ideas

            else:

                st.warning(
                    "Please select a field first."
                )

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

            if st.button(
                "Use Generated Ideas"
            ):

                st.session_state[
                    "selected_research_idea"
                ] = {
                    "title":
                    "Generated Research Ideas",
                    "description":
                    st.session_state[
                        "generated_ideas"
                    ],
                    "source":
                    "AI"
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
