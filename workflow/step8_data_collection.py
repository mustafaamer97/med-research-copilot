import pandas as pd
import streamlit as st
from modules.context_manager import get_context, update_context
from modules.questionnaire_builder import generate_questionnaire

COLLECTION_METHODS = [
    "Survey",
    "Hospital Records",
    "Registry Database",
    "Electronic Health Records (EHR)",
    "Laboratory Data",
    "Clinical Examination",
    "Questionnaire",
    "Imaging Data",
]


def infer_variable_type(variable: str) -> str:
    """استنتاج نوع المتغير تلقائياً بناءً على اسمه."""
    var_lower = variable.lower()
    if var_lower in ["sex", "gender", "smoking"]:
        return "Categorical"
    if any(x in var_lower for x in ["death", "mortality", "admission"]):
        return "Binary"
    return "Numeric"


def render():
    st.header("📝 Data Collection Plan")

    st.info(
        """
Define how study data will be collected
before starting recruitment.
"""
    )

    context = get_context()

    # 1. معالجة نوع research_question للأمان
    research_question = context.get("research_question_data") or {}
    protocol = context.get("research_protocol", "")
    sample_plan = context.get("sample_size_plan", {})

    # ملء ملخص البحث تلقائياً من Context
    with st.expander("📋 Research Summary", expanded=True):
        st.write(f"**Population:** {context.get('population', 'N/A')}")
        st.write(f"**Outcome:** {context.get('outcome', 'N/A')}")
        st.write(f"**Study Design:** {context.get('final_study_design', 'N/A')}")
        st.write(
            f"**Target Sample Size:** {context.get('total_sample_size', sample_plan.get('total_sample', 'N/A'))}"
        )

    st.markdown("---")

    variables = st.text_area(
        "Variables to Collect",
        height=180,
        placeholder="""
Age
Sex
BMI
Blood Pressure
HbA1c
Mortality
Hospital Admission
""",
    )

    collection_method = st.selectbox("Collection Method", COLLECTION_METHODS)

    estimated_duration = st.number_input(
        "Estimated Data Collection Duration (Months)",
        min_value=1,
        max_value=120,
        value=6,
    )

    default_sample_size = context.get(
        "total_sample_size", sample_plan.get("total_sample", 100)
    )

    try:
        default_sample_size = int(default_sample_size)
    except (ValueError, TypeError):
        default_sample_size = 100

    expected_sample_size = st.number_input(
        "Expected Sample Size", min_value=1, value=default_sample_size
    )

    # ==================================
    # Variable Classification
    # ==================================

    st.subheader("Variable Classification")

    variable_list = [v.strip() for v in variables.split("\n") if v.strip()]

    demographics = []
    outcomes = []
    exposures = []
    confounders = []

    for var in variable_list:
        lower = var.lower()

        if lower in ["age", "sex", "gender"]:
            demographics.append(var)
        elif any(
            x in lower for x in ["mortality", "death", "admission", "outcome"]
        ):
            outcomes.append(var)
        elif any(x in lower for x in ["bmi", "smoking", "treatment", "exposure"]):
            exposures.append(var)
        else:
            confounders.append(var)

    c1, c2 = st.columns(2)

    with c1:
        st.write("### Demographics")
        st.write(demographics)

        st.write("### Exposure Variables")
        st.write(exposures)

    with c2:
        st.write("### Outcome Variables")
        st.write(outcomes)

        st.write("### Confounders")
        st.write(confounders)

    # ==================================
    # Summary Metrics (الإضافة الذكية)
    # ==================================

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Variables", len(variable_list))
    m2.metric("Outcomes", len(outcomes))
    m3.metric("Exposures", len(exposures))

    # ==================================
    # Feasibility Score & Risk Assessment
    # ==================================

    score = 100

    if len(variable_list) > 20:
        score -= 20

    if expected_sample_size > 1000:
        score -= 30

    if estimated_duration > 24:
        score -= 20

    missing_risk = "Low"
    if len(variable_list) > 30:
        missing_risk = "High"
    elif len(variable_list) > 15:
        missing_risk = "Moderate"

    st.subheader("Data Collection Feasibility & Risk")

    col_score, col_risk = st.columns(2)

    with col_score:
        st.write("**Feasibility Score**")
        st.progress(max(0, score) / 100)
        if score >= 80:
            st.success("Easy Study")
        elif score >= 50:
            st.warning("Moderate Complexity")
        else:
            st.error("Complex Study")

    with col_risk:
        st.metric("Missing Data Risk", missing_risk)

    st.markdown("---")

    if st.button(
        "💾 Save Collection Plan", use_container_width=True, type="primary"
    ):
        # 5. حفظ Metadata موسعة داخل الخطة
        plan = {
            "variables": variables,
            "number_of_variables": len(variable_list),
            "method": collection_method,
            "collection_method": collection_method,
            "duration_months": estimated_duration,
            "study_duration_months": estimated_duration,
            "expected_sample_size": expected_sample_size,
            "demographics": demographics,
            "outcomes": outcomes,
            "exposures": exposures,
            "confounders": confounders,
            "feasibility_score": score,
            "missing_data_risk": missing_risk,
        }

        # 3. حفظ Classification المباشر داخل Data Dictionary
        dictionary = []
        for variable in variable_list:
            if variable in outcomes:
                category = "Outcome"
            elif variable in exposures:
                category = "Exposure"
            elif variable in demographics:
                category = "Demographic"
            else:
                category = "Confounder"

            dictionary.append(
                {
                    "Variable": variable,
                    "Type": infer_variable_type(variable),
                    "Category": category,
                    "Required": "Yes",
                }
            )

        # 4. حفظ عدد المتغيرات والشحنة الإحصائية الكاملة في Context
        update_context(
            data_collection_plan=plan,
            data_dictionary=dictionary,
            data_collection_completed=True,
            number_of_variables=len(variable_list),
            primary_outcomes=outcomes,
            exposure_variables=exposures,
            confounders=confounders,
        )

        st.success("Data collection plan saved successfully.")

    # إنشاء وتنزيل ملف Blank Dataset (CRF)
    if variable_list:
        crf = pd.DataFrame(columns=variable_list)
        st.download_button(
            "⬇️ Download Blank Dataset (CRF)",
            data=crf.to_csv(index=False),
            file_name="blank_dataset.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ==================================
    # Generate Questionnaire
    # ==================================

    st.markdown("---")
    if st.button("📝 Generate Questionnaire", use_container_width=True):
        with st.spinner("Generating questionnaire..."):
            questionnaire = generate_questionnaire(
                research_context=context,
                research_question=research_question,
                protocol=protocol,
                sample_size_plan=sample_plan,
                research_gaps=context.get("research_gaps", []),
            )

        update_context(research_questionnaire=questionnaire)
        st.rerun()

    questionnaire = context.get("research_questionnaire")

    if questionnaire:
        st.subheader("Generated Questionnaire")
        st.markdown(questionnaire)

        st.download_button(
            "⬇️ Download Questionnaire",
            data=questionnaire,
            file_name="research_questionnaire.md",
            use_container_width=True,
        )

        # ==================================
        # Google Forms Preparation
        # ==================================

        st.markdown("---")

        if st.button("🚀 Prepare Google Form", use_container_width=True):
            update_context(google_form_ready=True)
            st.success("Questionnaire prepared for Google Forms integration.")

        if context.get("google_form_ready"):
            st.info(
                """
Google Forms integration is configured.

When Google API connection is enabled,
this questionnaire will be converted
into a Google Form automatically.
"""
            )

    # ==================================
    # Data Dictionary Display
    # ==================================

    saved_dict = context.get("data_dictionary")
    if saved_dict:
        st.subheader("Data Dictionary")
        st.dataframe(saved_dict, use_container_width=True)

    # ==================================
    # Current Plan Display
    # ==================================

    saved_plan = context.get("data_collection_plan")
    if saved_plan:
        st.subheader("Current Collection Plan")
        st.json(saved_plan)

    if context.get("data_collection_completed"):
        st.success("✅ Step 8 Completed")
