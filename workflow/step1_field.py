import streamlit as st

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
    "Mixed Sources": [d for d in STUDY_DESIGNS if d != "Auto Detect"],
}

# 4. دالة مساعدة لتقييم جدوى البحث
def render_feasibility(validation):
    st.markdown("---")
    st.subheader("Research Feasibility Assessment")

    if not validation:
        st.info("Complete Disease, Outcome, and select a valid Study Design to view Feasibility Score.")
        return

    score = validation.get("score", 0)
    level = validation.get("feasibility", "Unknown").upper()

    if level == "HIGH":
        st.success(f"Feasibility Score: {score}/100 | Feasibility Level: HIGH")
    elif level == "MODERATE":
        st.warning(f"Feasibility Score: {score}/100 | Feasibility Level: MODERATE")
    else:
        st.error(f"Feasibility Score: {score}/100 | Feasibility Level: LOW")

    if validation.get("notes"):
        with st.expander("Why was this score assigned?"):
            for note in validation["notes"]:
                st.write(f"• {note}")

# 5. دالة لبناء قاموس السياق (Context Builder)
def build_context(
    research_type, analysis, target_population, exposure_or_intervention,
    comparison, outcome, study_objective, research_goal, study_design,
    recommended_design, data_source, disease, location, study_period, keywords
):
    return {
        "research_type": research_type,
        "research_category": (
            analysis["research_category"] if analysis else research_type
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
        "pico": {
            "population": target_population,
            "intervention": exposure_or_intervention,
            "comparison": comparison,
            "outcome": outcome,
            "topic": disease,
            "goal": research_goal,
            "study_design": study_design,
        },
    }

def render():
    saved_context = st.session_state.get("research_context", {})

    st.header("🧭 Research Context & Scope")
    st.write("Define your research area before building the research question.")

    st.subheader("Research Basics")

    # استرجاع Research Type
    saved_type = saved_context.get("research_type", RESEARCH_TYPES[0])
    type_index = RESEARCH_TYPES.index(saved_type) if saved_type in RESEARCH_TYPES else 0
    research_type = st.selectbox("Research Type", RESEARCH_TYPES, index=type_index)

    # استرجاع Data Source
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

    # استرجاع Research Goal
    saved_goal = saved_context.get("research_goal", RESEARCH_GOALS[0])
    goal_index = RESEARCH_GOALS.index(saved_goal) if saved_goal in RESEARCH_GOALS else 0
    research_goal = st.selectbox("Research Goal", RESEARCH_GOALS, index=goal_index)

    # 9. إدارة التحليل الذكي وتجنب إعادة الحساب (Caching)
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

        # 3. إزالة التكرار: عرض Field و Recommended Design فقط
        st.markdown("### 🤖 Research Detection")
        st.success(f"**Field:** {analysis['field']}\n\n**Recommended Design:** {recommended_design}")

    target_population = st.text_input(
        "Target Population",
        value=saved_context.get(
            "population",
            analysis["population"] if analysis and analysis.get("population") else ""
        ),
        placeholder="Breast cancer patients"
    )

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

    outcome = st.text_input(
        "Primary Outcome",
        value=saved_context.get("outcome", ""),
        placeholder="Incidence, Mortality, Survival..."
    )

    study_objective = st.text_area(
        "Study Objective",
        value=saved_context.get("objective", "")
    )

    # 10. جعل Recommended Design افتراضياً مع خيار التجاوز اليدوي (Override Design)
    selected_design = saved_context.get("study_design", recommended_design if recommended_design else "Cross-Sectional Study")
    
    with st.expander("⚙️ Override Study Design (Optional)", expanded=False):
        design_options = [d for d in STUDY_DESIGNS if d != "Auto Detect"]
        override_index = design_options.index(selected_design) if selected_design in design_options else 0
        override_choice = st.selectbox(
            "Select Alternative Study Design",
            design_options,
            index=override_index
        )
        if override_choice:
            study_design = override_choice
    
    if 'study_design' not in locals():
        study_design = selected_design

    # Study Design Validation
    allowed_designs = VALID_DESIGNS.get(
        data_source,
        [d for d in STUDY_DESIGNS if d != "Auto Detect"]
    )

    design_is_valid = study_design in allowed_designs

    if not design_is_valid:
        st.error(
            f"""
❌ Selected study design is not compatible with the chosen data source.
Data Source: {data_source}
Allowed Designs: {", ".join(allowed_designs)}
"""
        )

    study_period = st.text_input(
        "Study Period",
        value=saved_context.get("study_period", ""),
        placeholder="2015-2025"
    )

    default_keywords = (
        ", ".join(analysis["keywords"])
        if analysis and analysis.get("keywords")
        else ""
    )

    # 6. إصلاح زر Refresh Keywords مع الحفظ الصحيح في Session State
    col_kw_1, col_kw_2 = st.columns([4, 1])
    with col_kw_1:
        current_keywords_val = st.session_state.get(
            "temp_keywords",
            saved_context.get("keywords", default_keywords)
        )
        keywords = st.text_area("Keywords", value=current_keywords_val, height=120)
    
    with col_kw_2:
        st.write(" ")
        st.write(" ")
        if st.button("🔄 Refresh Keywords", help="Regenerate keywords based on current topic"):
            st.session_state["temp_keywords"] = default_keywords
            if "research_context" in st.session_state:
                st.session_state["research_context"]["keywords"] = default_keywords
            st.rerun()

    # 5. بناء السياق عبر الدالة
    context = build_context(
        research_type, analysis, target_population, exposure_or_intervention,
        comparison, outcome, study_objective, research_goal, study_design,
        recommended_design, data_source, disease, location, study_period, keywords
    )

    validation = None
    if disease and outcome and design_is_valid:
        validation = validate_research_idea(disease, context)

    if validation:
        context["context_quality_score"] = validation["score"]

    # 4. التقييم بواسطة الدالة المساعدة
    render_feasibility(validation)

    # Final Research Context Card
    st.markdown("---")
    st.subheader("📋 Final Research Context Card")
    st.info(
        f"""
**Disease / Topic:** {disease if disease else 'Not specified'}  
**Research Type:** {research_type} | **Goal:** {research_goal}  
**Data Source:** {data_source} | **Design:** {study_design}  
**Location:** {location if location else 'Not specified'} | **Period:** {study_period if study_period else 'Not specified'}  

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

    required_fields = [disease, target_population, outcome, study_period, keywords]
    if research_type == "Primary Research":
        required_fields.append(location)

    can_save = all(str(x).strip() for x in required_fields) and design_is_valid

    if can_save:
        if st.button("💾 Save Research Context", use_container_width=True, type="primary"):
            # 7. حفظ القاموس والقيم الفردية داخل Session State
            st.session_state["context_completed"] = True
            st.session_state["research_context"] = context
            st.session_state["disease"] = disease
            st.session_state["population"] = target_population
            st.session_state["study_design"] = study_design
            st.session_state["field"] = context["field"]

            # 8. إشعارات هادئة بدون Balloons
            st.toast("Research Context Saved", icon="✅")
            st.rerun()
    else:
        if not design_is_valid:
            st.warning("Cannot save: Selected study design is incompatible with the chosen data source.")
        else:
            st.warning("Please complete Disease, Target Population, Location, Outcome, Study Period and Keywords to continue.")

    if st.session_state.get("context_completed"):
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
