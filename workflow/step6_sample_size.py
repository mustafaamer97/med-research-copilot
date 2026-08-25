import plotly.express as px
import streamlit as st

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

    st.info(
        """
Estimate the required sample size
before starting the study.
"""
    )

    study_type = st.selectbox(
        "Study Type",
        [
            "RCT",
            "Cohort",
            "Case-Control",
            "Cross-Sectional"
        ]
    )

    effect_size = st.number_input(
        "Expected Effect Size (Cohen's d)",
        min_value=0.1,
        max_value=2.0,
        value=0.5,
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

            n = calculate_sample_size(
                effect_size,
                alpha,
                power
            )

            total_n = n * 2

            st.success(
                f"""
Required sample size per group: {n}

Total sample size: {total_n}
"""
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

            st.session_state[
                "sample_size_plan"
            ] = {
                "study_type": study_type,
                "effect_size": effect_size,
                "alpha": alpha,
                "power": power,
                "per_group": n,
                "total_sample": total_n
            }

            st.session_state[
                "sample_size_completed"
            ] = True

        except Exception as e:

            st.error(str(e))

    plan = st.session_state.get(
        "sample_size_plan"
    )

    if plan:

        st.subheader(
            "Current Sample Size Plan"
        )

        st.json(plan)

    if st.session_state.get(
        "sample_size_completed"
    ):

        st.success(
            "✅ Step 6 Completed"
        )
