import streamlit as st
from modules.pico_builder import build_pico


def render():

    st.info(
        "Workflow validation is temporarily disabled during development."
    )

    st.header(
        "🧬 PICO Research Question Builder"
    )

    idea_data = st.session_state.get(
        "selected_research_idea",
        {}
    )

    if idea_data:

        st.info(
            f"""
Selected Research Idea

Title:
{idea_data.get('title', '')}

Description:
{idea_data.get('description', '')}
"""
        )

    population = st.text_input("Population (P)")
    intervention = st.text_input("Intervention (I)")
    comparison = st.text_input("Comparison (C)")
    outcome = st.text_input("Outcome (O)")

    if st.button(
        "Generate Research Question"
    ):

        result = build_pico(
            population,
            intervention,
            comparison,
            outcome
        )

        st.session_state[
            "generated_question"
        ] = result

    if "generated_question" in st.session_state:

        result = st.session_state[
            "generated_question"
        ]

        st.subheader(
            "Research Question"
        )

        st.write(
            result["question"]
        )

        st.subheader(
            "Search Strategy"
        )

        st.code(
            result["keywords"]
        )

        if st.button(
            "Save Research Question",
            use_container_width=True,
            type="primary"
        ):

            st.session_state[
                "research_question"
            ] = result

            st.session_state[
                "question_completed"
            ] = True

            st.success(
                "Research Question saved successfully."
            )

            st.rerun()
