import plotly.express as px
import streamlit as st

# 1) استيراد إدارة Context Manager
from modules.context_manager import (
    get_context,
    update_context
)
from research_analytics.power_curve import (
    build_power_curve
)
from research_analytics.sample_size_engine import (
    calculate_sample_size
)


def render():

    st.header(
        "📊 Sample Size & Statistical Power"
    )

    # 2) الحصول على Context بدلاً من session_state المباشر
    context = get_context()
    research_context = context

    # 3) تحديد نوع الدراسة الافتراضي من Step5 أولاً
    default_study = (
        context.get("final_study_design")
        or context.get("study_design")
        or "RCT"
    )

    # 4) إضافة Research Summary
    with st.expander(
        "📋 Research Summary",
        expanded=True
    ):
        st.write(
            f"**Disease:** {context.get('disease', '')}"
        )
        st.write(
            f"**Population:** {context.get('population', '')}"
        )
        st.write(
            f"**Outcome:** {context.get('outcome', '')}"
        )
        st.write(
            f"**Study Design:** {default_study}"
        )
        st.write(
            f"**Location:** {context.get('location', '')}"
        )

    st.info(
        """
Estimate the required sample size
before starting the study.
"""
    )

    # ==================================
    # Auto Fill Study Design
    # ==================================

    default_index = 0

    if "Cohort" in default_study:
        default_index = 1
    elif "Case-Control" in default_study:
        default_index = 2
    elif "Cross-Sectional" in default_study:
        default_index = 3

    study_type = st.selectbox(
        "Study Type",
        [
            "RCT",
            "Cohort",
            "Case-Control",
            "Cross-Sectional"
        ],
        index=default_index
    )

    # ==================================
    # Suggested Analysis
    # ==================================

    st.subheader(
        "Suggested Statistical Analysis"
    )

    if study_type == "RCT":
        st.write("• Intention-To-Treat Analysis")
        st.write("• T-Test")
        st.write("• ANOVA")
        st.write("• Effect Size")

    elif study_type == "Cohort":
        st.write("• Kaplan-Meier Analysis")
        st.write("• Cox Regression")
        st.write("• Hazard Ratios")

    elif study_type == "Case-Control":
        st.write("• Odds Ratios")
        st.write("• Chi-Square Test")
        st.write("• Logistic Regression")

    elif study_type == "Cross-Sectional":
        st.write("• Descriptive Statistics")
        st.write("• Chi-Square Test")
        st.write("• Logistic Regression")

    # ==================================
    # Effect Size Guide
    # ==================================

    st.subheader(
        "Effect Size Guide"
    )

    st.info(
        """
Small Effect = 0.2

Medium Effect = 0.5

Large Effect = 0.8
"""
    )

    # 5) اقتراح حجم الأثر بناءً على Evidence Count
    suggested_effect = 0.5
    if context.get("evidence_count", 0) > 20:
        suggested_effect = 0.3

    effect_size = st.number_input(
        "Expected Effect Size (Cohen's d)",
        min_value=0.1,
        max_value=2.0,
        value=suggested_effect,
        step=0.1
    )

    alpha = st.number_input(
        "Alpha",
        min_value=0.01,
        max_value=0.20,
        value=0.05,
        step=0.01
    )

    power = st.number_input(
        "Power",
        min_value=0.50,
        max_value=0.99,
        value=0.80,
        step=0.05
    )

    if st.button(
        "Calculate Sample Size",
        type="primary",
        use_container_width=True
    ):

        try:
            # 10) إضافة study_type للدالة
            n = calculate_sample_size(
                study_type=study_type,
                effect_size=effect_size,
                alpha=alpha,
                power=power
            )

            total_n = n * 2

            st.success(
                f"""
Required sample size per group: {n}

Total sample size: {total_n}
"""
            )

            # ==================================
            # Interpretation
            # ==================================

            if total_n < 100:
                st.warning(
                    "Small sample study"
                )
            elif total_n < 500:
                st.success(
                    "Moderate sample study"
                )
            else:
                st.info(
                    "Large sample study"
                )

            curve_df = build_power_curve(
                effect_size,
                alpha
            )

            fig = px.line(
                curve_df,
                x="Power",
                y="Sample Size",
                markers=True,
                title="Power Curve"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # 6 & 7) حفظ النتائج وتحديث الـ Context بدون الاعتماد المباشر على session_state
            sample_plan = {
                "study_type": study_type,
                "effect_size": effect_size,
                "alpha": alpha,
                "power": power,
                "per_group": n,
                "total_sample": total_n
            }

            update_context(
                sample_size_plan=sample_plan,
                sample_size_completed=True,
                target_sample_size=total_n
            )

        except Exception as e:
            st.error(str(e))

    # 8) قراءة الخطة الحالية من context
    plan = context.get(
        "sample_size_plan"
    )

    if plan:
        st.subheader(
            "Current Sample Size Plan"
        )
        st.json(plan)

    # 9) التحقق من الإكمال باستخدام context
    if context.get(
        "sample_size_completed"
    ):
        st.success(
            "✅ Step 6 Completed"
        )
