import streamlit as st

from modules.idea_validator import (
    validate_research_idea
)
from modules.medical_knowledge_engine import (
    analyze_research_topic
)

def recommend_study_design(
    data_source,
    outcome,
    default_design="Cross-Sectional Study"
):

    outcome = outcome.lower()

    if data_source == "Registry Database":

        if any(
            x in outcome
            for x in [
                "trend",
                "incidence",
                "prevalence",
                "distribution"
            ]
        ):

            return (
                "Retrospective Registry-Based Study",
                [
                    "Cross-Sectional Study",
                    "Retrospective Cohort Study"
                ]
            )

        return (
            "Retrospective Cohort Study",
            [
                "Cross-Sectional Study"
            ]
        )

    if data_source == "Hospital Records":

        return (
            "Retrospective Cohort Study",
            [
                "Case-Control Study",
                "Cross-Sectional Study"
            ]
        )

    # تعديل (6): تم تصحيح المطابقة لتكون "Published Literature"
    if data_source == "Published Literature":

        return (
            "Systematic Review",
            [
                "Meta-Analysis"
            ]
        )

    return (
        default_design,
        []
    )

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

# تعديل (2): تم حذف القوائم غير المستخدمة FIELD_KEYWORD_HINTS و TARGET_POPULATIONS

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

    disease = st.text_input(
        "Disease / Research Topic",
        placeholder="Cancer, Diabetes, Stroke..."
    )

    location = st.text_input(
        "Study Location",
        placeholder="Sana'a, Yemen"
    )

    outcome = st.text_input(
        "Primary Outcome",
        placeholder="Incidence, Mortality, Survival, Risk Factors..."
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

    data_source = st.selectbox(
        "Available Data Source",
        DATA_SOURCES
    )

    analysis = None

    if disease:
        # تعديل (3): حماية التطبيق من الانهيار في حال فشل تحليل الـ AI
        try:
            analysis = analyze_research_topic(
                topic=disease,
                goal=research_goal,
                data_source=data_source,
            )
        except Exception:
            analysis = None

        if analysis:
            st.markdown(
                "### 🤖 Research Detection"
            )

            st.success(
                f"""
Field:
{analysis['field']}

Population:
{analysis['population']}

Recommended Design:
{analysis['recommended_design']}
"""
            )

    if study_design == "Auto Detect" and analysis:

        study_design = analysis["recommended_design"]

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

    recommended_design = None
    alternative_designs = []

    if outcome:

        recommended_design, alternative_designs = (
            recommend_study_design(
                data_source,
                outcome,
                default_design=analysis["recommended_design"]
                if analysis
                else study_design
            )
        )

    study_period = st.text_input(
        "Study Period",
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
        value=", ".join(
            analysis["keywords"]
        )
        if analysis
        else "",
        height=120,
    )

    context = {

        "field": analysis["field"]
        if analysis
        else "",

        "population": analysis["population"]
        if analysis
        else "",

        "research_goal": research_goal,

        "study_design": study_design,

        "recommended_design":
        analysis["recommended_design"]
        if analysis
        else "",

        "data_source": data_source,

        "disease": disease,

        "location": location,

        "outcome": outcome,

        "study_period": study_period,

        "keywords": keywords,

    }

    # تعديل (4): توسيع نطاق الـ Session State لدعم الخطوات القادمة
    st.session_state["research_context"] = context
    st.session_state["research_field"] = context.get(
        "field",
        ""
    )
    st.session_state["research_population"] = context.get(
        "population",
        ""
    )
    st.session_state["research_goal"] = research_goal
    st.session_state["research_outcome"] = outcome
    st.session_state["research_disease"] = disease

    # تعديل (1): التمرير الصحيح للمُدخلات لدالة التقييم
    validation = validate_research_idea(
        disease,
        context
    )

    # تعديل (8): حفظ نتائج الـ Validation لاستخدامها في بقية الخطوات
    st.session_state[
        "context_validation"
    ] = validation

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

    if validation["feasibility"] == "High":

        st.success(
            f"""
Feasibility Score: {validation['score']}/100

Feasibility Level: HIGH
"""
        )

    elif validation["feasibility"] == "Moderate":

        st.warning(
            f"""
Feasibility Score: {validation['score']}/100

Feasibility Level: MODERATE
"""
        )

    else:

        st.error(
            f"""
Feasibility Score: {validation['score']}/100

Feasibility Level: LOW
"""
        )

    if validation["notes"]:

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

    required_fields = [
        disease,
        location,
        outcome,
        study_period,
        keywords
    ]

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

            # تعديل (7): فحص جودة السياق البحثي قبل الحفظ لمنع الاستمرار بحالة ضعيفة
            if validation["score"] < 50:
                st.error(
                    "Research context quality is too low. Please improve the study design or data source."
                )
                st.stop()

            # تعديل (5): تحديث حالة الخطوة ورقم الخطوة الحالية لنظام 13 خطوة
            st.session_state[
                "context_completed"
            ] = True
            st.session_state[
                "current_step"
            ] = 1

            st.success(
                "Research context saved successfully."
            )

    else:

        st.warning(
            "Please complete Disease, Location, Outcome, Study Period and Keywords to continue."
        )

    if st.session_state.get(
        "context_completed"
    ):

        st.success(
            "✅ Step 1 Completed"
        )
