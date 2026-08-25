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

        default_field = (
            st.session_state.get(
                "research_context",
                {}
            ).get(
                "field",
                ""
            )
        )

        field = st.text_input(
            "Medical Field",
            value=default_field
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
            "Enter your existing research idea."
        )

        idea_title = st.text_input(
            "Research Idea Title"
        )

        idea_description = st.text_area(
            "Research Idea Description"
        )

        if st.button(
            "Save Research Idea"
        ):

            st.session_state[
                "selected_research_idea"
            ] = {
                "title": idea_title,
                "description": idea_description,
                "source": "manual"
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
