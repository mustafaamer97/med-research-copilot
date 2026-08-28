import streamlit as st

from modules.pico_builder import (
    build_pico
)

# =========================
# التعديل 3: Dynamic Framework Detection
# =========================
def detect_framework(
    study_design
):
    design = (
        study_design or ""
    ).lower()
    if "systematic review" in design:
        return "PEO"
    if "meta-analysis" in design:
        return "PEO"
    if "diagnostic" in design:
        return "PIRT"
    if "prognostic" in design:
        return "PICOTS"
    if "prediction" in design:
        return "PICOTS"
    if "cross-sectional" in design:
        return "PEO"
    if "case-control" in design:
        return "PEO"
    if "cohort" in design:
        return "PEO"
    return "PICO"


def render():

    # =========================
    # التعديل 1: تغيير عنوان الصفحة
    # =========================
    st.header(
        "🧬 Research Question Framework Builder"
    )

    st.info(
        "Build a structured research question tailored to your study design."
    )

    # =========================
    # Display Selected Idea
    # =========================

    idea_data = st.session_state.get(
        "selected_research_idea",
        {}
    )

    # Extracted Data from Step 2 (Flexible context fallback)
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

    # =========================
    # التعديل 2 & 4: عرض Study Design و Recommended Question Framework
    # =========================
    study_design = (
        context.get(
            "recommended_design"
        )
        or context.get(
            "study_design"
        )
        or ""
    )
    st.info(
        f"""
Study Design:
{study_design}
"""
    )

    framework = detect_framework(
        study_design
    )
    st.success(
        f"""
Recommended Question Framework:
{framework}
"""
    )

    default_population = context.get(
        "population",
        ""
    )

    population_default = default_population

    population = st.text_input(
        "Population (P)",
        value=population_default
    )

    # Auto-fill Intervention from Step 2
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

    # =========================
    # التعديل 5: إضافة Research Factor
    # =========================
    research_factor = st.text_input(
        "Exposure / Risk Factor"
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

        # =========================
        # التعديل 6: تعديل بناء السؤال عبر تمرير research_goal و study_design
        # =========================
        result = build_pico(
            population,
            intervention,
            comparison,
            outcome,
            study_design,
            context.get(
                "research_goal",
                ""
            )
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

            # =========================
            # التعديل 8: إضافة Study Design للبحث بدلاً من Period (التعديل 7)
            # =========================
            if study_design:

                pubmed_query_parts.append(
                    f'("{study_design}")'
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
                        study_design
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
                        study_design
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
                        research_factor,
                        comparison,
                        outcome_text,
                        population,
                        study_design
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

        # =========================
        # التعديل 11: عرض Framework في قسم النتيجة
        # =========================
        st.write(
            f"Framework Used: {framework}"
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

                # =========================
                # التعديل 9 & 10: حفظ Framework والانتقال المباشر إلى Step 4
                # =========================
                st.session_state[
                    "research_question"
                ] = {
                    **result,
                    "framework": framework,
                    "pico": {
                        "population": population,
                        "intervention": intervention,
                        "research_factor": research_factor,
                        "comparison": comparison,
                        "outcome": outcome,
                        "study_design": study_design
                    },
                    "context": context
                }

                st.session_state[
                    "question_completed"
                ] = True

                st.session_state[
                    "current_step"
                ] = 4

                st.success(
                    "Research Question saved successfully."
                )

                st.info(
                    "Next Step: Literature Search"
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
