import plotly.express as px
import streamlit as st

# استيراد إدارة Context Manager
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
from research_analytics.study_design_mapper import (
    get_recommended_statistics
)


def render():

    st.header(
        "📊 Sample Size & Statistical Power"
    )

    # 1) الحصول على Context
    context = get_context()

    # تحديد نوع الدراسة الافتراضي من Step5 أولاً
    default_study = (
        context.get("final_study_design")
        or context.get("study_design")
        or "RCT"
    )

    # إضافة Research Summary
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

    for item in get_recommended_statistics(
        study_type
    ):
        st.write(f"• {item}")

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

    # حماية قيمة suggested_effect وجلبها من Context أو اقتراحها
    suggested_effect = context.get(
        "suggested_effect_size",
        0.5
    )
    if (
        not context.get("suggested_effect_size")
        and context.get("evidence_count", 0) > 20
    ):
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

    # التحقق من إكمال الخطوة الخامسة لمنع القفز المباشر
    protocol_completed = context.get("protocol_completed", False) or bool(
        st.session_state.get("research_protocol")
    )

    if not protocol_completed:
        st.warning(
            "⚠️ Please complete Step 5 (Protocol Builder) first to enable sample size calculation."
        )

    if st.button(
        "Calculate Sample Size",
        disabled=not protocol_completed,
        type="primary",
        use_container_width=True
    ):

        try:
            # حساب حجم العينة
            n = calculate_sample_size(
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

            # إضافة مصدر التقدير evidence_count وبقية الـ Metadata
            sample_plan = {
                "study_type": study_type,
                "effect_size": effect_size,
                "alpha": alpha,
                "power": power,
                "per_group": n,
                "total_sample": total_n,
                "calculation_method": "TTestIndPower",
                "allocation_ratio": 1,
                "evidence_count": context.get(
                    "evidence_count",
                    0
                )
            }

            # التحديث الشامل للـ Context وإضافة protocol_completed=True
            update_context(
                sample_size_plan=sample_plan,
                sample_size_recommendation=sample_plan,
                sample_size_per_group=n,
                total_sample_size=total_n,
                power=power,
                alpha=alpha,
                effect_size=effect_size,
                final_study_design=study_type,
                sample_size_completed=True,
                target_sample_size=total_n,
                protocol_completed=True
            )

            # حفظ الخطة داخل session_state للتوافق
            st.session_state["sample_size_plan"] = sample_plan
            st.session_state["sample_size_completed"] = True

            # إعادة تحميل الصفحة لتحديث واجهة المستخدم
            st.rerun()

        except Exception as e:
            st.error(str(e))

    # ==================================
    # قراءة الخطة الحالية
    # ==================================

    plan = context.get(
        "sample_size_plan"
    ) or st.session_state.get(
        "sample_size_plan"
    )

    protocol = st.session_state.get(
        "research_protocol",
        ""
    )

    if protocol:
        current_total_n = (
            context.get("total_sample_size")
            or (plan.get("total_sample", 0) if plan else 0)
        )
        st.info(
            f"""
Protocol Generated ✅

Recommended Design:
{study_type}

Suggested Total Sample:
{current_total_n}
"""
        )

    if plan:
        st.subheader(
            "Current Sample Size Plan"
        )
        st.json(plan)

    # التحقق من الإكمال
    if context.get(
        "sample_size_completed"
    ) or st.session_state.get(
        "sample_size_completed"
    ):
        st.success(
            "✅ Step 6 Completed"
        )
