import streamlit as st

from modules.pico_builder import (
    build_pico
)


def render():

    st.header(
        "🧬 Research Question Builder"
    )

    st.info(
        "Build a structured PICO research question."
    )

    # =========================
    # Display Selected Idea
    # =========================

    idea_data = st.session_state.get(
        "selected_research_idea",
        {}
    )

    default_disease = idea_data.get(
        "disease",
        ""
    )

    default_location = idea_data.get(
        "location",
        ""
    )

    default_outcome = idea_data.get(
        "outcome",
        ""
    )

    default_period = idea_data.get(
        "period",
        ""
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

    # =========================
    # Defaults from Step 1
    # =========================

    context = st.session_state.get(
        "research_context",
        {}
    )

    default_population = context.get(
        "population",
        ""
    )

    population_default = default_population

    if default_disease:

        population_default = (
            f"{default_population} with {default_disease}"
        )

    population = st.text_input(
        "Population (P)",
        value=population_default
    )

    intervention = st.text_input(
        "Intervention (I)"
    )

    comparison = st.text_input(
        "Comparison (C)"
    )

    outcome = st.text_input(
        "Outcome (O)",
        value=default_outcome
    )

    # =========================
    # Study Context
    # =========================

    st.subheader(
        "Study Context"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.write(
            f"**Disease:** {default_disease}"
        )

        st.write(
            f"**Location:** {default_location}"
        )

    with c2:

        st.write(
            f"**Outcome:** {default_outcome}"
        )

        st.write(
            f"**Period:** {default_period}"
        )

    # =========================
    # Generate Question
    # =========================

    if st.button(
        "Generate Research Question",
        use_container_width=True
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

            st.session_state[
                "generated_question"
            ] = result

    # =========================
    # Display Result
    # =========================

    result = st.session_state.get(
        "generated_question"
    )

    if result:

        st.subheader(
            "Research Question"
        )

        st.success(
            result["question"]
        )

        st.subheader(
            "PubMed Search Strategy"
        )

        st.code(
            result["keywords"],
            language="text"
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

    # =========================
    # Completion Status
    # =========================

    if st.session_state.get(
        "question_completed"
    ):

        st.success(
            "✅ Step 3 Completed"
        )
