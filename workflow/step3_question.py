import streamlit as st

from modules.pico_builder import (
    build_pico
)


def render():

    st.header(
        "🧬 Research Question Builder"
    )

    st.info(
        "Build a structured research question based on your selected idea."
    )

    # ==================================
    # Selected Idea
    # ==================================

    idea_data = st.session_state.get(
        "selected_research_idea",
        {}
    )

    if idea_data:

        with st.expander(
            "Selected Research Idea",
            expanded=True
        ):

            st.markdown(
                f"""
### {idea_data.get('title', '')}

{idea_data.get('description', '')}
"""
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Disease:** {idea_data.get('disease', 'Not specified')}"
                )

                st.write(
                    f"**Location:** {idea_data.get('location', 'Not specified')}"
                )

            with col2:

                st.write(
                    f"**Outcome:** {idea_data.get('outcome', 'Not specified')}"
                )

                st.write(
                    f"**Period:** {idea_data.get('period', 'Not specified')}"
                )

    # ==================================
    # Defaults From Previous Steps
    # ==================================

    context = st.session_state.get(
        "research_context",
        {}
    )

    default_population = context.get(
        "population",
        ""
    )

    default_outcome = idea_data.get(
        "outcome",
        ""
    )

    # ==================================
    # PICO Builder
    # ==================================

    st.subheader(
        "PICO Framework"
    )

    population = st.text_input(
        "Population (P)",
        value=default_population
    )

    intervention = st.text_input(
        "Intervention / Exposure (I)"
    )

    comparison = st.text_input(
        "Comparison (C)"
    )

    outcome = st.text_input(
        "Outcome (O)",
        value=default_outcome
    )

    # ==================================
    # Preview
    # ==================================

    st.markdown("### Research Components")

    preview_text = f"""
Population:
{population}

Intervention / Exposure:
{intervention}

Comparison:
{comparison}

Outcome:
{outcome}
"""

    st.info(preview_text)

    # ==================================
    # Generate Question
    # ==================================

    if st.button(
        "Generate Research Question",
        use_container_width=True,
        type="primary"
    ):

        result = build_pico(
            population,
            intervention,
            comparison,
            outcome
        )

        if "error" in result:

            st.error(
                result["error"]
            )

        else:

            result[
                "disease"
            ] = idea_data.get(
                "disease",
                ""
            )

            result[
                "location"
            ] = idea_data.get(
                "location",
                ""
            )

            result[
                "period"
            ] = idea_data.get(
                "period",
                ""
            )

            result[
                "study_design"
            ] = context.get(
                "study_design",
                ""
            )

            result[
                "field"
            ] = context.get(
                "field",
                ""
            )

            st.session_state[
                "generated_question"
            ] = result

    # ==================================
    # Display Result
    # ==================================

    result = st.session_state.get(
        "generated_question"
    )

    if result:

        st.subheader(
            "Generated Research Question"
        )

        st.success(
            result["question"]
        )

        st.subheader(
            "Literature Search Strategy"
        )

        st.code(
            result["keywords"],
            language="text"
        )

        st.caption(
            "This search strategy will be used in Step 4 across PubMed, Europe PMC and OpenAlex."
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save Research Question",
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

        with col2:

            st.download_button(
                "⬇️ Download Question",
                data=result["question"],
                file_name="research_question.txt",
                use_container_width=True
            )

    # ==================================
    # Completion Status
    # ==================================

    if st.session_state.get(
        "question_completed"
    ):

        st.success(
            "✅ Step 3 Completed"
        )
