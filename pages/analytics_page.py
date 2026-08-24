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
        "📊 Research Analytics"
    )

    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is None:
        return

    # =========================
    # Load Dataset & Analyze
    # =========================

    df, report = analyze_dataset(
        uploaded_file
    )

    st.success(
        "Dataset loaded successfully"
    )

    # =========================
    # Dataset Preview
    # =========================

    st.subheader(
        "Dataset Preview"
    )

    st.dataframe(
        df.head()
    )

    # =========================
    # Data Checker Information
    # =========================

    st.subheader(
        "Dataset Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Rows",
            report["rows"]
        )

        st.metric(
            "Columns",
            report["columns"]
        )

    with col2:

        st.metric(
            "Duplicates",
            report["duplicates"]
        )

        st.metric(
            "Numeric Variables",
            len(
                report[
                    "numeric_columns"
                ]
            )
        )

    st.divider()

    # =========================
    # Variable Selection
    # =========================

    group_col = st.selectbox(
        "Grouping Variable",
        df.columns
    )

    outcome_col = st.selectbox(
        "Outcome Variable",
        report[
            "numeric_columns"
        ]
    )

    # =========================
    # Smart Analysis
    # =========================

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

        # =====================
        # Statistical Analysis
        # =====================

        result = run_analysis(
            df=df,
            test_name=recommendation["test"],
            group_col=group_col,
            outcome_col=outcome_col
        )

        st.subheader(
            "Statistical Results"
        )

        st.dataframe(
            result
        )

        # =====================
        # Academic Report
        # =====================

        report_text = (
            generate_academic_report(
                recommendation["test"],
                result
            )
        )

        st.subheader(
            "Academic Report"
        )

        st.write(
            report_text
        )
