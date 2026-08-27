import streamlit as st

from modules.idea_validator import validate_research_idea
from modules.medical_knowledge_engine import analyze_research_topic
from modules.study_design_classifier import recommend_study_design

MEDICAL_FIELDS = [
    "Cardiology",
    "Neurology",
    "Oncology",
    "Endocrinology",
    "Gastroenterology",
    "Pulmonology",
    "Nephrology",
    "Infectious Diseases",
    "Psychiatry",
    "Dermatology",
    "Pediatrics",
    "Obstetrics & Gynecology",
    "General Surgery",
    "Orthopedic Surgery",
    "Neurosurgery",
    "Urology",
    "Ophthalmology",
    "Otolaryngology (ENT)",
    "Emergency Medicine",
    "Public Health",
]

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

    st.write("Define your research area before building the research question.")

    st.subheader("Research Basics")

    disease = st.text_input("Disease / Research Topic", placeholder="Cancer, Diabetes, Stroke...")

    location = st.text_input("Study Location", placeholder="Sana'a, Yemen")

    outcome = st.text_input(
        "Primary Outcome", placeholder="Incidence, Mortality, Survival, Risk Factors..."
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
        ],
    )

    study_design = st.selectbox("Study Design", STUDY_DESIGNS)

    data_source = st.selectbox("Available Data Source", DATA_SOURCES)

    analysis = None

    # تنظيف المُدخلات النصية مباشرة باستخدام .strip()
    clean_disease = disease.strip()
    clean_location = location.strip()
    clean_outcome = outcome.strip()

    if clean_disease:
        try:
            analysis = analyze_research_topic(
                topic=clean_disease,
                goal=research_goal,
                data_source=data_source,
            )
        except Exception:
            analysis = None

        if analysis:
            st.markdown("### 🤖 Research Detection")

            st.success(
                f"""
Field:
{analysis.get('field', '')}

Population:
{analysis.get('population', '')}

Recommended Design:
{analysis.get('recommended_design', '')}
"""
            )

    if study_design == "Auto Detect" and analysis:
        auto_detected_design = analysis.get("recommended_design", "")

        st.info(
            f"""
🤖 Auto detected study design:

{auto_detected_design}
"""
        )

    # ==================================
    # Study Design Validation
    # ==================================

    allowed_designs = VALID_DESIGNS.get(data_source, STUDY_DESIGNS)

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

    study_period = st.text_input("Study Period", placeholder="2015-2025")
    clean_study_period = study_period.strip()

    keywords = st.text_area(
        "Keywords",
        value=", ".join(analysis["keywords"]) if analysis and "keywords" in analysis else "",
        height=120,
    )
    clean_keywords = keywords.strip()

    # ==================================
    # Initial Context Assembly (cleaned)
    # ==================================
    context = {
        "field": analysis.get("field", "") if analysis else "",
        "population": analysis.get("population", "") if analysis else "",
        "research_goal": research_goal,
        "study_design": study_design,
        "data_source": data_source,
        "disease": clean_disease,
        "location": clean_location,
        "outcome": clean_outcome,
        "period": clean_study_period,
        "study_period": clean_study_period,  # إضافة المسميين معاً
        "keywords": clean_keywords,
    }

    # ==================================
    # Study Design Classification Engine
    # ==================================
    design_result = recommend_study_design(context)

    context["recommended_design"] = design_result.get("recommended_design", "")

    # عدم استبدال اختيار المستخدم إلا إذا كان "Auto Detect"
    if study_design == "Auto Detect":
        context["study_design"] = design_result.get("recommended_design", study_design)
    else:
        context["study_design"] = study_design

    context["study_design_confidence"] = design_result.get("confidence", "Medium")
    context["study_design_reasons"] = design_result.get("reasons", [])
    context["study_design_warnings"] = design_result.get("warnings", [])

    # ==================================
    # Save Context to Session State
    # ==================================
    st.session_state["research_context"] = context

    # ==================================
    # Additional Session State Updates
    # ==================================
    st.session_state["research_field"] = context.get("field", "")
    st.session_state["research_population"] = context.get("population", "")
    st.session_state["research_goal"] = research_goal
    st.session_state["research_outcome"] = clean_outcome
    st.session_state["research_disease"] = clean_disease

    validation = validate_research_idea(clean_disease, context)
    st.session_state["context_validation"] = validation

    # ==================================
    # Recommendations UI Display
    # ==================================
    if context.get("recommended_design"):
        st.markdown("---")
        st.subheader("📚 Methodology Recommendation")

        st.success(
            f"**Recommended Design:** {context['recommended_design']}\n\n"
            f"**Confidence Level:** {context['study_design_confidence']}"
        )

        if context.get("study_design_reasons"):
            with st.expander("Why was this design recommended?"):
                for reason in context["study_design_reasons"]:
                    st.write(f"• {reason}")

        if context.get("study_design_warnings"):
            for warning in context["study_design_warnings"]:
                st.warning(f"⚠️ {warning}")

    st.markdown("---")
    st.subheader("Research Feasibility Assessment")

    if validation.get("feasibility") == "High":
        st.success(
            f"""
Feasibility Score: {validation.get('score', 0)}/100

Feasibility Level: HIGH
"""
        )
    elif validation.get("feasibility") == "Moderate":
        st.warning(
            f"""
Feasibility Score: {validation.get('score', 0)}/100

Feasibility Level: MODERATE
"""
        )
    else:
        st.error(
            f"""
Feasibility Score: {validation.get('score', 0)}/100

Feasibility Level: LOW
"""
        )

    if validation.get("notes"):
        with st.expander("Why was this score assigned?"):
            for note in validation["notes"]:
                st.write(f"• {note}")

    st.markdown("---")
    st.subheader("Research Context Summary")

    st.info(
        f"""
**Research Goal:** {research_goal}

**Selected Study Design:** {context['study_design']}

**Recommended Study Design:** {context['recommended_design']}

**Data Source:** {data_source}

**Disease / Topic:** {clean_disease if clean_disease else 'Not specified'}

**Study Location:** {clean_location if clean_location else 'Not specified'}

**Primary Outcome:** {clean_outcome if clean_outcome else 'Not specified'}

**Study Period:** {clean_study_period if clean_study_period else 'Not specified'}

**Keywords:** {clean_keywords if clean_keywords else 'Not specified'}
"""
    )

    required_fields = [
        clean_disease,
        clean_location,
        clean_outcome,
        clean_study_period,
        clean_keywords,
    ]

    if clean_disease and data_source:
        disease_lower = clean_disease.lower()
        if (
            "cancer" in disease_lower
            or "tumor" in disease_lower
            or "neoplasm" in disease_lower
        ):
            st.info("Detected possible Oncology project.")
        elif "diabetes" in disease_lower:
            st.info("Detected possible Endocrinology project.")
        elif "stroke" in disease_lower:
            st.info("Detected possible Neurology project.")

    if all(x for x in required_fields):
        if st.button(
            "💾 Save Research Context",
            use_container_width=True,
            type="primary",
        ):
            if validation.get("score", 0) < 50:
                st.error(
                    "Research context quality is too low. Please improve the study design or data source."
                )
                st.stop()

            st.session_state["context_completed"] = True
            st.session_state["current_step"] = 1

            st.success("Research context saved successfully.")
    else:
        st.warning(
            "Please complete Disease, Location, Outcome, Study Period and Keywords to continue."
        )

    if st.session_state.get("context_completed"):
        st.success("✅ Step 1 Completed")
