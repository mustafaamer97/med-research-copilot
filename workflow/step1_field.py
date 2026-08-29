import streamlit as st

from modules.idea_validator import (
    validate_research_idea
)
from modules.medical_knowledge_engine import (
    analyze_research_topic
)


STUDY_DESIGNS = [

    "Auto Detect",

    "Cross-Sectional Study",
    "Case-Control Study",
    "Prospective Cohort Study",
    "Retrospective Cohort Study",
    "Nested Case-Control Study",
    "Case-Cohort Study",

    "Randomized Controlled Trial (RCT)",
    "Cluster Randomized Trial",
    "Pragmatic Clinical Trial",
    "Adaptive Clinical Trial",

    "Diagnostic Accuracy Study",
    "Prediction Model Study",
    "Prognostic Study",

    "Survey Study",
    "Ecological Study",
    "Registry-Based Study",

    "Interrupted Time Series",
    "Before-After Study",

    "Case Report",
    "Case Series",

    "Systematic Review",
    "Meta-Analysis",
    "Network Meta-Analysis",
    "Scoping Review",
    "Umbrella Review",

    "Qualitative Study",
    "Mixed Methods Study",

    "Health Services Research",
    "Implementation Study",
    "Quality Improvement Study",
]

DATA_SOURCES = [
    "Hospital Records",
    "Registry Database",
    "Electronic Health Records (EHR)",
    "Survey / Questionnaire",
    "Laboratory Data",
    "Imaging Data",
    "Published Literature",
    "Mixed Sources",
]

VALID_DESIGNS = {

    "Registry Database": [
        "Auto Detect",
        "Registry-Based Study",
        "Cross-Sectional Study",
        "Case-Control Study",
        "Prospective Cohort Study",
        "Retrospective Cohort Study",
        "Interrupted Time Series",
    ],

    "Hospital Records": [
        "Auto Detect",
        "Cross-Sectional Study",
        "Case-Control Study",
        "Retrospective Cohort Study",
        "Case Series",
    ],

    "Electronic Health Records (EHR)": [
        "Auto Detect",
        "Retrospective Cohort Study",
        "Prediction Model Study",
        "Diagnostic Accuracy Study",
    ],

    "Survey / Questionnaire": [
        "Auto Detect",
        "Survey Study",
        "Cross-Sectional Study",
        "Mixed Methods Study",
    ],

    "Published Literature": [
        "Auto Detect",
        "Systematic Review",
        "Meta-Analysis",
        "Network Meta-Analysis",
        "Scoping Review",
    ],

    "Mixed Sources": STUDY_DESIGNS,

}


def render():

    st.header("🧭 Research Context & Scope")

    st.write(
        "Define your research area before building the research question."
    )

    st.subheader(
        "Research Basics"
    )

    research_type = st.selectbox(
        "Research Type",
        [
            "Primary Research",
            "Secondary Research",
            "Evidence Synthesis"
        ]
    )

    if research_type == "Primary Research":

        data_source = st.selectbox(
            "Available Data Source",
            DATA_SOURCES
        )

    else:

        data_source = "Published Literature"

        st.info(
            "Data source automatically set to Published Literature."
        )

    disease = st.text_input(
        "Disease / Research Topic",
        value=st.session_state.get("disease", ""),
        placeholder="Cancer, Diabetes, Stroke..."
    )

    target_population = st.text_input(
        "Target Population",
        value=st.session_state.get("population", ""),
        placeholder="Breast cancer patients"
    )

    exposure_or_intervention = st.text_input(
        "Exposure / Intervention",
        value=st.session_state.get("intervention", "")
    )

    comparison = st.text_input(
        "Comparator",
        value=st.session_state.get("comparison", "")
    )

    location = st.text_input(
        "Study Location",
        value=st.session_state.get("location", ""),
        placeholder="Sana'a, Yemen"
    )

    outcome = st.text_input(
        "Primary Outcome",
        value=st.session_state.get("outcome", ""),
        placeholder="Incidence, Mortality, Survival..."
    )

    study_objective = st.text_area(
        "Study Objective",
        value=st.session_state.get("study_objective", "")
    )

    research_goal = st.selectbox(
        "Research Goal",
        [
            "Trend Analysis",
            "Incidence",
            "Prevalence",
            "Risk Factors",
            "Treatment Outcomes",
            "Survival Analysis",
            "Diagnostic Accuracy",
            "Prediction Model",
            "Systematic Review",
        ]
    )

    study_design = st.selectbox(
        "Study Design",
        STUDY_DESIGNS
    )

    analysis = None
    recommended_design = None
    alternative_designs = []

    if disease:

        analysis = analyze_research_topic(
            topic=disease,
            goal=research_goal,
            data_source=data_source,
        )

        st.markdown(
            "### 🤖 Research Detection"
        )

        st.success(
            f"""
Field:
{analysis['field']}

Population:
{analysis['population']}
"""
        )

        recommended_design = analysis.get("recommended_design")
        alternative_designs = analysis.get("alternative_designs", [])

    if (
        study_design == "Auto Detect"
        and recommended_design
    ):

        study_design = recommended_design

        st.info(
            f"""
🤖 Auto detected study design:

{study_design}
"""
        )

    # ==================================
    # Study Design Validation
    # ==================================

    allowed_designs = VALID_DESIGNS.get(
        data_source,
        STUDY_DESIGNS
    )

    if study_design not in allowed_designs:

        st.error(
            f"""
❌ Selected study design is not compatible
with the chosen data source.

Data Source:
{data_source}

Allowed Designs:
{", ".join(allowed_designs)}
"""
        )

    study_period = st.text_input(
        "Study Period",
        value=st.session_state.get("study_period", ""),
        placeholder="2015-2025"
    )

    auto_keywords = []

    for item in [
        disease,
        outcome,
        research_goal,
    ]:
        if item:
            auto_keywords.append(item)

    keywords = st.text_area(
        "Keywords",
        value=st.session_state.get(
            "keywords",
            ", ".join(analysis["keywords"]) if analysis else ""
        ),
        height=120,
    )

    context = {
        "research_type": research_type,
        "research_category": (
            analysis["research_category"]
            if analysis
            else research_type
        ),
        "field": analysis["field"] if analysis else "",
        "population": target_population,
        "intervention": exposure_or_intervention,
        "comparison": comparison,
        "outcome": outcome,
        "objective": study_objective,
        "research_goal": research_goal,
        "study_design": study_design,
        "recommended_design": recommended_design if recommended_design else "",
        "data_source": data_source,
        "disease": disease,
        "location": location,
        "study_period": study_period,
        "keywords": keywords,
    }

    # التعديل الرابع: التحقق فقط عند توفر Disease و Outcome معاً لتقليل الضغط
    validation = None
    if disease and outcome:
        validation = validate_research_idea(
            disease,
            context
        )

    if validation:
        context["context_quality_score"] = validation["score"]

    if recommended_design:

        st.markdown("---")

        st.subheader(
            "📚 Methodology Recommendation"
        )

        st.success(
            f"""
Recommended Design:

{recommended_design}
"""
        )

        if alternative_designs:

            st.info(
                "Alternative Designs:\n\n• "
                + "\n• ".join(
                    alternative_designs
                )
            )

    if (
        recommended_design
        and study_design
        and study_design != recommended_design
    ):

        st.warning(
            f"""
The selected study design differs
from the recommended methodology.

Recommended:
{recommended_design}

Selected:
{study_design}
"""
        )

    st.markdown("---")

    st.subheader(
        "Research Feasibility Assessment"
    )

    if validation and validation["feasibility"] == "High":

        st.success(
            f"""
Feasibility Score: {validation['score']}/100

Feasibility Level: HIGH
"""
        )

    elif validation and validation["feasibility"] == "Moderate":

        st.warning(
            f"""
Feasibility Score: {validation['score']}/100

Feasibility Level: MODERATE
"""
        )

    elif validation:

        st.error(
            f"""
Feasibility Score: {validation['score']}/100

Feasibility Level: LOW
"""
        )

    if validation and validation["notes"]:

        with st.expander(
            "Why was this score assigned?"
        ):

            for note in validation["notes"]:

                st.write(f"• {note}")

    st.markdown("---")

    st.subheader(
        "Research Context Summary"
    )

    st.info(
        f"""
**Research Type:** {research_type}

**Target Population:** {target_population if target_population else 'Not specified'}

**Exposure / Intervention:** {exposure_or_intervention if exposure_or_intervention else 'Not specified'}

**Comparator:** {comparison if comparison else 'Not specified'}

**Study Objective:** {study_objective if study_objective else 'Not specified'}

**Research Goal:** {research_goal}

**Study Design:** {study_design}

**Data Source:** {data_source}

**Disease / Topic:** {disease if disease else 'Not specified'}

**Study Location:** {location if location else 'Not specified'}

**Primary Outcome:** {outcome if outcome else 'Not specified'}

**Study Period:** {study_period if study_period else 'Not specified'}

**Keywords:** {keywords if keywords else 'Not specified'}
"""
    )

    st.markdown("---")

    st.subheader("🧩 Preliminary PICO")

    st.info(
        f"""
P = {target_population}

I = {exposure_or_intervention}

C = {comparison}

O = {outcome}
"""
    )

    required_fields = [
        disease,
        target_population,
        outcome,
        study_period,
        keywords
    ]

    if research_type == "Primary Research":

        required_fields.append(
            location
        )

    if disease and data_source:

        if (
            "cancer" in disease.lower()
            or "tumor" in disease.lower()
            or "neoplasm" in disease.lower()
        ):

            st.info(
                "Detected possible Oncology project."
            )

        elif "diabetes" in disease.lower():

            st.info(
                "Detected possible Endocrinology project."
            )

        elif "stroke" in disease.lower():

            st.info(
                "Detected possible Neurology project."
            )

    if all(str(x).strip() for x in required_fields):

        if st.button(
            "💾 Save Research Context",
            use_container_width=True,
            type="primary",
        ):

            st.session_state["context_completed"] = True
            st.session_state["research_context"] = context

            st.session_state["disease"] = disease
            st.session_state["population"] = target_population
            st.session_state["intervention"] = exposure_or_intervention
            st.session_state["comparison"] = comparison
            st.session_state["outcome"] = outcome
            st.session_state["location"] = location
            st.session_state["study_period"] = study_period
            st.session_state["keywords"] = keywords
            st.session_state["study_objective"] = study_objective
            st.session_state["research_type"] = research_type
            st.session_state["field"] = analysis["field"] if analysis else ""
            st.session_state["study_design"] = study_design
            st.session_state["data_source"] = data_source
            st.session_state["pico"] = {
                "population": target_population,
                "intervention": exposure_or_intervention,
                "comparison": comparison,
                "outcome": outcome,
                "topic": disease,
                "goal": research_goal,
                "study_design": study_design
            }

            st.success(
                "Research context saved successfully."
            )

            st.rerun()

    else:

        st.warning(
            "Please complete Disease, Target Population, Location, Outcome, Study Period and Keywords to continue."
        )

    if st.session_state.get(
        "context_completed"
    ):

        st.success(
            "✅ Step 1 Completed"
        )
