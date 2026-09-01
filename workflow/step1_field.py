import re
import streamlit as st

from modules.context_manager import (
    get_context,
    update_context,
    mark_completed,
    is_completed
)
from modules.idea_validator import validate_research_idea
from modules.medical_knowledge_engine import analyze_research_topic

RESEARCH_TYPES = [
    "Primary Research",
    "Secondary Research",
    "Evidence Synthesis"
]

RESEARCH_GOALS = [
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
        "Registry-Based Study",
        "Cross-Sectional Study",
        "Case-Control Study",
        "Prospective Cohort Study",
        "Retrospective Cohort Study",
        "Interrupted Time Series",
    ],
    "Hospital Records": [
        "Cross-Sectional Study",
        "Case-Control Study",
        "Retrospective Cohort Study",
        "Case Series",
    ],
    "Electronic Health Records (EHR)": [
        "Retrospective Cohort Study",
        "Prediction Model Study",
        "Diagnostic Accuracy Study",
    ],
    "Survey / Questionnaire": [
        "Survey Study",
        "Cross-Sectional Study",
        "Mixed Methods Study",
    ],
    "Published Literature": [
        "Systematic Review",
        "Meta-Analysis",
        "Network Meta-Analysis",
        "Scoping Review",
    ],
    "Mixed Sources": [
        "Cross-Sectional Study",
        "Case-Control Study",
        "Prospective Cohort Study",
        "Retrospective Cohort Study",
        "Randomized Controlled Trial (RCT)",
        "Diagnostic Accuracy Study",
        "Prediction Model Study",
        "Systematic Review",
        "Meta-Analysis",
    ],
}

# التحسين الثالث: الأهداف الافتراضية التلقائية بناءً على هدف البحث
AUTO_OBJECTIVES = {
    "Trend Analysis": "Evaluate temporal trends of the selected outcome over the study period.",
    "Incidence": "Estimate disease incidence and demographic distribution in the target population.",
    "Prevalence": "Estimate disease prevalence and associated clinical characteristics.",
    "Risk Factors": "Identify clinical and environmental factors associated with the selected outcome.",
    "Treatment Outcomes": "Assess treatment efficacy, safety, and therapeutic outcomes.",
    "Survival Analysis": "Evaluate long-term survival rates and identify predictors of mortality.",
    "Diagnostic Accuracy": "Evaluate sensitivity, specificity, and overall diagnostic performance.",
    "Prediction Model": "Develop and validate a predictive risk model for the primary outcome.",
    "Systematic Review": "Synthesize available literature to summarize evidence on the research topic.",
}


def render_feasibility(validation):
    st.markdown("---")
    st.subheader("Research Feasibility Assessment")

    if not validation:
        st.info("Complete Disease, Outcome, and select a valid Study Design to view Feasibility Score.")
        return

    score = validation.get("score", 0)
    level = validation.get("feasibility", "Unknown").upper()

    if score >= 90:
        st.success(f"🟢 Excellent Research Context (Score: {score}/100)")
    elif score >= 75:
        st.info(f"🟡 Good Research Context (Score: {score}/100)")
    else:
        st.warning(f"🟠 Needs Improvement (Score: {score}/100)")

    if level == "HIGH":
        st.write("Feasibility Level: **HIGH**")
    elif level == "MODERATE":
        st.write("Feasibility Level: **MODERATE**")
    else:
        st.write("Feasibility Level: **LOW**")

    if validation.get("notes"):
        with st.expander("Why was this score assigned?"):
            for note in validation["notes"]:
                st.write(f"• {note}")


def build_context(analysis, form_data):
    return {
        "research_type": form_data["research_type"],
        "research_category": (
            analysis["research_category"] if analysis else form_data["research_type"]
        ),
        "field": analysis["field"] if analysis else "",
        "population": form_data["target_population"],
        "intervention": form_data["exposure_or_intervention"],
        "comparison": form_data["comparison"],
        "outcome": form_data["outcome"],
        "objective": form_data["study_objective"],
        "research_goal": form_data["research_goal"],
        "study_design": form_data["study_design"],
        "recommended_design": analysis.get("recommended_design", "") if analysis else "",
        "data_source": form_data["data_source"],
        "disease": form_data["disease"],
        "location": form_data["location"],
        "study_period": form_data["study_period"],
        "keywords": form_data["keywords"],
        "confidence": analysis["confidence"] if analysis and "confidence" in analysis else 0,
        "confidence_level": analysis["confidence_level"] if analysis and "confidence_level" in analysis else "Unknown",
        "pico": {
            "population": form_data["target_population"],
            "intervention": form_data["exposure_or_intervention"],
            "comparison": form_data["comparison"],
            "outcome": form_data["outcome"],
            "topic": form_data["disease"],
            "goal": form_data["research_goal"],
            "study_design": form_data["study_design"],
        },
    }


def render():
    saved_context = get_context()

    st.header("🧭 Research Context & Scope")
    st.write("Define your research area before building the research question.")

    st.subheader("Research Basics")

    saved_type = saved_context.get("research_type", RESEARCH_TYPES[0])
    type_index = RESEARCH_TYPES.index(saved_type) if saved_type in RESEARCH_TYPES else 0
    research_type = st.selectbox("Research Type", RESEARCH_TYPES, index=type_index)

    if research_type == "Primary Research":
        saved_source = saved_context.get("data_source", DATA_SOURCES[0])
        source_index = DATA_SOURCES.index(saved_source) if saved_source in DATA_SOURCES else 0
        data_source = st.selectbox("Available Data Source", DATA_SOURCES, index=source_index)
    else:
        data_source = "Published Literature"
        st.info("Data source automatically set to Published Literature.")

    disease = st.text_input(
        "Disease / Research Topic",
        value=saved_context.get("disease", ""),
        placeholder="Cancer, Diabetes, Stroke..."
    )

    saved_goal = saved_context.get("research_goal", RESEARCH_GOALS[0])
    goal_index = RESEARCH_GOALS.index(saved_goal) if saved_goal in RESEARCH_GOALS else 0
    research_goal = st.selectbox("Research Goal", RESEARCH_GOALS, index=goal_index)

    analysis = None
    recommended_design = None

    if disease:
        cache_key = f"{disease}_{research_goal}_{data_source}"
        if st.session_state.get("analysis_cache_key") == cache_key:
            analysis = st.session_state.get("analysis_cache")
        else:
            analysis = analyze_research_topic(
                topic=disease,
                goal=research_goal,
                data_source=data_source,
            )
            st.session_state["analysis_cache"] = analysis
            st.session_state["analysis_cache_key"] = cache_key

        recommended_design = analysis.get("recommended_design")

        st.markdown("### 🤖 Research Detection")
        col_det_1, col_det_2 = st.columns([3, 1])
        with col_det_1:
            st.success(
                f"""
**Field:** {analysis['field']}  
**Research Category:** {analysis['research_category']}  
**Recommended Design:** {recommended_design}
"""
            )
        with col_det_2:
            conf_val = analysis.get("confidence", 0)
            conf_lvl = analysis.get("confidence_level", "Unknown")
            st.metric("Confidence", f"{conf_val}%")
            st.caption(f"Level: {conf_lvl}")

    auto_population = analysis["population"] if analysis and analysis.get("population") else ""
    target_population = st.text_input(
        "Target Population",
        value=saved_context.get("population", auto_population),
        placeholder="Breast cancer patients"
    )
    st.caption("Auto-detected population. You may edit if needed.")

    exposure_or_intervention = st.text_input(
        "Exposure / Intervention",
        value=saved_context.get("intervention", "")
    )

    comparison = st.text_input(
        "Comparator",
        value=saved_context.get("comparison", "")
    )

    location = st.text_input(
        "Study Location",
        value=saved_context.get("location", ""),
        placeholder="Sana'a, Yemen"
    )

    suggested_outcomes = analysis.get("suggested_outcomes", []) if analysis else []
    outcome_options = suggested_outcomes + ["Other..."] if suggested_outcomes else ["Other..."]
    
    saved_outcome = saved_context.get("outcome", "")
    
    if saved_outcome and saved_outcome in suggested_outcomes:
        outcome_default_idx = outcome_options.index(saved_outcome)
    else:
        outcome_default_idx = len(outcome_options) - 1

    selected_outcome_option = st.selectbox(
        "Primary Outcome (Select or Enter Custom)",
        outcome_options,
        index=outcome_default_idx
    )

    if selected_outcome_option == "Other...":
        outcome = st.text_input(
            "Specify Custom Primary Outcome",
            value=saved_outcome if saved_outcome not in suggested_outcomes else "",
            placeholder="Incidence, Mortality, Survival..."
        )
    else:
        outcome = selected_outcome_option

    # التحسين الثالث: تطبيق Auto Objective بناءً على Goal في حال عدم وجود هدف مدخل
    default_auto_obj = AUTO_OBJECTIVES.get(research_goal, "")
    study_objective = st.text_area(
        "Study Objective",
        value=saved_context.get("objective", default_auto_obj)
    )

    available_designs = VALID_DESIGNS.get(data_source, VALID_DESIGNS["Mixed Sources"])

    selected_design = saved_context.get("study_design", recommended_design if recommended_design in available_designs else available_designs[0])
    study_design = selected_design

    with st.expander("⚙️ Override Study Design (Optional)", expanded=False):
        override_index = available_designs.index(study_design) if study_design in available_designs else 0
        override_choice = st.selectbox(
            "Select Alternative Study Design",
            available_designs,
            index=override_index
        )
        if override_choice:
            study_design = override_choice

    design_is_valid = study_design in available_designs

    if not design_is_valid:
        st.error(
            f"""
❌ Selected study design is not compatible with the chosen data source.
Data Source: {data_source}
Allowed Designs: {", ".join(available_designs)}
"""
        )

    study_period = st.text_input(
        "Study Period",
        value=saved_context.get("study_period", ""),
        placeholder="2015-2025"
    )
    
    valid_period = bool(re.match(r"^\d{4}\s*-\s*\d{4}$", study_period.strip())) if study_period.strip() else True
    if study_period.strip() and not valid_period:
        st.warning("⚠️ Please use format: YYYY-YYYY (e.g., 2015-2025)")

    default_keywords = (
        ", ".join(analysis["keywords"])
        if analysis and analysis.get("keywords")
        else ""
    )

    col_kw_1, col_kw_2 = st.columns([4, 1])
    with col_kw_1:
        current_keywords = saved_context.get("keywords", default_keywords)
        keywords = st.text_area("Keywords", value=current_keywords, height=120)

    with col_kw_2:
        st.write(" ")
        st.write(" ")
        if st.button("🔄 Refresh Keywords", help="Regenerate keywords based on current topic"):
            if "research_context" not in st.session_state:
                st.session_state["research_context"] = {}
            st.session_state["research_context"]["keywords"] = default_keywords
            st.rerun()

    form_data = {
        "research_type": research_type,
        "data_source": data_source,
        "disease": disease,
        "research_goal": research_goal,
        "target_population": target_population,
        "exposure_or_intervention": exposure_or_intervention,
        "comparison": comparison,
        "location": location,
        "outcome": outcome,
        "study_objective": study_objective,
        "study_design": study_design,
        "study_period": study_period,
        "keywords": keywords,
    }

    context = build_context(analysis, form_data)

    validation = None
    if disease and outcome and design_is_valid:
        # التحسين الأول: تعديل الاستدعاء ليمرر context فقط
        validation = validate_research_idea(context)

    if validation:
        context["context_quality_score"] = validation["score"]

    render_feasibility(validation)

    st.markdown("---")
    st.subheader("📋 Final Research Context Card")
    st.info(
        f"""
**Disease / Topic:** {disease if disease else 'Not specified'}  
**Research Type:** {research_type} | **Category:** {context.get('research_category', 'N/A')}  
**Goal:** {research_goal} | **Data Source:** {data_source} | **Design:** {study_design}  
**Location:** {location if location else 'Not specified'} | **Period:** {study_period if study_period else 'Not specified'}  
**Detection Confidence:** {context.get('confidence', 0)}% ({context.get('confidence_level', 'N/A')}) | **Context Quality Score:** {context.get('context_quality_score', 'N/A')}/100  

---

#### 🧩 Preliminary PICO
* **P (Population):** {target_population if target_population else 'Not specified'}
* **I (Intervention / Exposure):** {exposure_or_intervention if exposure_or_intervention else 'Not specified'}
* **C (Comparator):** {comparison if comparison else 'Not specified'}
* **O (Outcome):** {outcome if outcome else 'Not specified'}

---

**Objective:** {study_objective if study_objective else 'Not specified'}  
**Keywords:** {keywords if keywords else 'Not specified'}
"""
    )

    # الحقول المطلوبة لشرط الحفظ
    required_fields = [disease, target_population, outcome, study_period, keywords, study_objective]
    if research_type == "Primary Research":
        required_fields.append(location)

    # التحسين الرابع: حساب دقيق وموزون لـ Readiness Score
    # 80% للحقول الإلزامية الأساسية و 20% للحقول الاختيارية المفيدة (PICO completeness)
    core_completed = sum(1 for x in required_fields if str(x).strip())
    core_score = (core_completed / len(required_fields)) * 80

    optional_fields = [exposure_or_intervention, comparison]
    optional_completed = sum(1 for x in optional_fields if str(x).strip())
    optional_score = (optional_completed / len(optional_fields)) * 20

    readiness_percentage = round(core_score + optional_score)
    
    st.markdown("### 📊 Step 1 Completion Progress")
    st.progress(readiness_percentage / 100)
    st.write(f"**Research Readiness:** {readiness_percentage}%")

    can_save = all(str(x).strip() for x in required_fields) and design_is_valid and valid_period

    if can_save:
        if st.button(
            "💾 Save Research Context",
            use_container_width=True,
            type="primary"
        ):
            update_context(**context)
            mark_completed("context")
            # Temporary compatibility layer
            st.session_state["context_completed"] = True
            st.session_state["disease"] = disease
            st.session_state["population"] = target_population
            st.session_state["study_design"] = study_design
            st.session_state["field"] = context["field"]
            st.session_state["research_goal"] = research_goal
            st.session_state["data_source"] = data_source
            st.session_state["outcome"] = outcome
            st.session_state["location"] = location
            st.session_state["study_period"] = study_period
            st.session_state["keywords"] = keywords

            # التحسين الثاني: حفظ Confidence و Confidence Level في session_state
            st.session_state["confidence"] = context.get("confidence", 0)
            st.session_state["confidence_level"] = context.get("confidence_level", "Unknown")

            st.toast("Research Context Saved", icon="✅")
            st.rerun()
    else:
        if not design_is_valid:
            st.warning("Cannot save: Selected study design is incompatible with the chosen data source.")
        elif not valid_period:
            st.warning("Cannot save: Study Period format must be YYYY-YYYY.")
        else:
            st.warning("Please complete Disease, Target Population, Location, Outcome, Study Objective, Study Period and Keywords to continue.")

    if is_completed("context"):
        st.markdown("---")
        st.success("✅ Step 1 Completed")

        ctx = st.session_state.get("research_context", {})
        st.info(
            f"""
**Disease / Topic:** {ctx.get('disease', 'N/A')}  
**Design:** {ctx.get('study_design', 'N/A')}  
**Population:** {ctx.get('population', 'N/A')}
"""
        )
