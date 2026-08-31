import streamlit as st

from modules.context_manager import (
    get_context,
    update_context
)

from modules.pico_builder import (
    build_pico
)

def render():

    st.header(
        "❓ Research Question Builder"
    )
    context = get_context()
    population = context.get(
        "population",
        ""
    )
    outcome = context.get(
        "outcome",
        ""
    )
    study_design = context.get(
        "study_design",
        ""
    )
    research_goal = context.get(
        "research_goal",
        ""
    )
    location = context.get(
        "location",
        ""
    )
    study_period = context.get(
        "study_period",
        ""
    )
    st.caption(
        "Generate a structured research question using PICO / PECO."
    )
    with st.expander(
        "Research Context",
        expanded=True
    ):
        st.write(
            f"**Population:** {population}"
        )
        st.write(
            f"**Outcome:** {outcome}"
        )
        st.write(
            f"**Study Design:** {study_design}"
        )
        st.write(
            f"**Research Goal:** {research_goal}"
        )
        st.write(
            f"**Location:** {location}"
        )
        st.write(
            f"**Study Period:** {study_period}"
        )
    intervention = st.text_input(
        "Intervention / Exposure",
        value=context.get(
            "intervention",
            ""
        )
    )
    comparison = st.text_input(
        "Comparison",
        value=context.get(
            "comparison",
            ""
        )
    )
    if st.button(
        "Generate Research Question",
        type="primary",
        use_container_width=True
    ):
        result = build_pico(
            population=population,
            intervention=intervention,
            comparison=comparison,
            outcome=outcome,
            study_design=study_design,
            research_goal=research_goal,
        )
        if result.get("error"):
            st.error(
                result["error"]
            )
            return
        
        result["location"] = location
        result["study_period"] = study_period
        
        update_context(
            intervention=intervention,
            comparison=comparison,
            research_question_data=result,
            question_completed=True
        )
        st.rerun()
    research_question = context.get(
        "research_question_data",
        {}
    )
    if research_question:
        st.divider()
        st.subheader(
            "Generated Research Question"
        )
        st.success(
            research_question.get(
                "question",
                ""
            )
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Framework",
                research_question.get(
                    "framework",
                    "PICO"
                )
            )
        with col2:
            st.metric(
                "Study Design",
                research_question.get(
                    "study_design",
                    ""
                )
            )
        st.subheader(
            "Search Keywords"
        )
        st.code(
            research_question.get(
                "keywords",
                ""
            )
        )
        st.subheader(
            "PICO / PECO Structure"
        )
        pico = research_question.get(
            "pico",
            {}
        )
        st.json(
            pico
        )
        st.success(
            "✅ Step 3 Completed"
        )
