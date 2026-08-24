import streamlit as st
import pandas as pd

from research_analytics.data_checker import (
    analyze_dataset
)

from research_analytics.smart_selector import (
    auto_select_group_comparison_test
)

from research_analytics.analysis_engine import (
    run_analysis
)

from research_analytics.report_generator import (
    generate_academic_report
)


def render():

    st.header(
        "📊 Automated Statistical Analysis"
    )

    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx"]
    )

    if not uploaded_file:
        return

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    _, report = analyze_dataset(
        uploaded_file
    )

    group_col = st.selectbox(
        "Grouping Variable",
        df.columns
    )

    outcome_col = st.selectbox(
        "Outcome Variable",
        df.columns
    )

    if st.button(
        "Run Smart Analysis"
    ):

        recommendation = (
            auto_select_group_comparison_test(
                df,
                report,
                group_col,
                outcome_col
            )
        )

        st.subheader(
            "AI Recommendation"
        )

        st.success(
            recommendation["test"]
        )

        st.write(
            recommendation["reason"]
        )

        result = run_analysis(
            df=df,
            test_name=
                recommendation["test"],
            group_col=group_col,
            outcome_col=outcome_col
        )

        st.subheader(
            "Statistical Results"
        )

        st.dataframe(result)

        report_text = (
            generate_academic_report(
                recommendation["test"],
                result
            )
        )

        st.subheader(
            "Academic Interpretation"
        )

        st.write(report_text)
