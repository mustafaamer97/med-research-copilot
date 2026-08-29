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

    # 1. Extracted Data from Step 2 (Flexible context fallback)
    default_topic = (
        idea_data.get("context", {}).get("disease")
        or idea_data.get("disease")
        or idea_data.get("topic")
        or ""
    )

    default_location = (
        idea_data.get("location")
        or idea_data.get("context", {}).get("location")
        or ""
    )

    default_outcome = (
        idea_data.get("outcome")
        or idea_data.get("context", {}).get("outcome")
        or ""
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
    # Defaults from Step 1 & Step 2
    # =========================

    context = st.session_state.get(
        "research_context",
        {}
    )

    default_population = context.get(
        "population",
        ""
    )

    # 2. Population default without hardcoded disease prefix
    population_default = default_population

    population = st.text_input(
        "Population (P)",
        value=population_default
    )

    # 3. Auto-fill Intervention from Step 2
    if idea_data:

        intervention_default = idea_data.get(
            "intervention",
            ""
        )

    else:

        intervention_default = ""

    intervention = st.text_input(
        "Intervention (I)",
        value=intervention_default
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

        # 4. Display Topic instead of hardcoded Disease
        st.write(
            f"**Research Topic:** {default_topic}"
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

    missing_context = []

    if not default_topic:

        missing_context.append(
            "Topic"
        )

    if not default_location:

        missing_context.append(
            "Location"
        )

    if not default_period:

        missing_context.append(
            "Period"
        )

    if missing_context:

        st.warning(
            "Missing context: "
            + ", ".join(missing_context)
        )

    # =========================
    # Generate Question
    # =========================

    if st.button(
        "Generate Research Question",
        use_container_width=True
    ):

        if not population.strip():

            st.warning(
                "Population is required."
            )

            return

        if not outcome.strip():

            st.warning(
                "Outcome is required."
            )

            return

        # Passing study_design with fallback to recommended_design, along with research_goal
        result = build_pico(
            population,
            intervention,
            comparison,
            outcome,
            context.get(
                "study_design",
                context.get(
                    "recommended_design",
                    ""
                )
            ),
            context.get("research_goal", "")
        )

        if "error" in result:

            st.error(
                result["error"]
            )

        else:

            location = idea_data.get(
                "location",
                ""
            )

            period = idea_data.get(
                "period",
                ""
            )

            outcome_text = outcome

            # =========================
            # PubMed Query
            # =========================

            pubmed_query_parts = []

            if default_topic.strip():

                pubmed_query_parts.append(
                    f'("{default_topic}"[Title/Abstract])'
                )

            if location:

                pubmed_query_parts.append(
                    f'("{location}"[Title/Abstract])'
                )

            if outcome_text:

                pubmed_query_parts.append(
                    f'("{outcome_text}"[Title/Abstract])'
                )

            if period:

                pubmed_query_parts.append(
                    f'("{period}"[Title/Abstract])'
                )

            pubmed_query = " AND ".join(
                pubmed_query_parts
            )

            # =========================
            # Europe PMC Query
            # =========================

            europe_pmc_query = " AND ".join(
                [
                    x
                    for x in [
                        default_topic,
                        location,
                        outcome_text,
                        period
                    ]
                    if x
                ]
            )

            # =========================
            # OpenAlex Query
            # =========================

            openalex_query = " ".join(
                [
                    x
                    for x in [
                        default_topic,
                        location,
                        outcome_text,
                        period
                    ]
                    if x
                ]
            )

            # =========================
            # Master Query
            # =========================

            master_query = " ".join(
                [
                    x
                    for x in [
                        default_topic,
                        location,
                        intervention,
                        comparison,
                        outcome_text,
                        population
                    ]
                    if x
                ]
            )

            if not pubmed_query:

                st.error(
                    "Unable to generate search query."
                )

                return

            result[
                "pubmed_query"
            ] = pubmed_query

            result[
                "europe_pmc_query"
            ] = europe_pmc_query

            result[
                "openalex_query"
            ] = openalex_query

            result[
                "master_query"
            ] = master_query

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
            "Literature Search Strategy"
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "PubMed",
                "Europe PMC",
                "OpenAlex"
            ]
        )

        with tab1:

            st.code(
                result.get(
                    "pubmed_query",
                    ""
                ),
                language="text"
            )

        with tab2:

            st.code(
                result.get(
                    "europe_pmc_query",
                    ""
                ),
                language="text"
            )

        with tab3:

            st.code(
                result.get(
                    "openalex_query",
                    ""
                ),
                language="text"
            )

        st.markdown(
            "### Master Search Query"
        )

        st.code(
            result.get(
                "master_query",
                ""
            ),
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
                ] = {
                    **result,
                    "pico": {
                        "population": population,
                        "intervention": intervention,
                        "comparison": comparison,
                        "outcome": outcome,
                        "study_design": context.get(
                            "study_design",
                            context.get(
                                "recommended_design",
                                ""
                            )
                        )
                    },
                    "context": context
                }

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
