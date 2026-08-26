import pandas as pd
import streamlit as st

from research_analytics.analysis_engine import (
    run_analysis,
)
from research_analytics.data_checker import (
    analyze_dataset,
)
from research_analytics.report_generator import (
    generate_academic_report,
)
from research_analytics.smart_selector import (
    auto_select_group_comparison_test,
)


def render():

    st.header("📊 Research Analytics")

    uploaded_file = st.file_uploader(
        "Upload Dataset", type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is None:
        return

    # =========================
    # Load Dataset & Analyze
    # =========================

    df, report = analyze_dataset(uploaded_file)

    st.success("Dataset loaded successfully")

    # =========================
    # Dataset Preview
    # =========================

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    # =========================
    # Data Checker Information
    # =========================

    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:

        st.metric("Rows", report["rows"])

        st.metric("Columns", report["columns"])

    with col2:

        st.metric("Duplicates", report["duplicates"])

        st.metric(
            "Numeric Variables",
            len(report["numeric_columns"])
        )

    st.divider()

    # =========================
    # Analysis Type Selection
    # =========================

    analysis_type = st.selectbox(
        "Analysis Type",
        [
            "Group Comparison",
            "Correlation Analysis",
            "Categorical Association",
            "Regression Analysis",
        ],
    )

    # =========================
    # Group Comparison
    # =========================

    if analysis_type == "Group Comparison":

        group_col = st.selectbox(
            "Grouping Variable",
            df.columns
        )

        outcome_col = st.selectbox(
            "Outcome Variable",
            report["numeric_columns"]
        )

        if st.button("Run Analysis"):

            recommendation = (
                auto_select_group_comparison_test(
                    df,
                    report,
                    group_col,
                    outcome_col
                )
            )

            st.success(
                recommendation["test"]
            )

            st.write(
                recommendation["reason"]
            )

            result = run_analysis(
                df=df,
                test_name=recommendation["test"],
                group_col=group_col,
                outcome_col=outcome_col,
            )

            # =====================================
            # Save Results for Step 11 Manuscript
            # =====================================

            st.session_state[
                "statistics_results"
            ] = result

            st.session_state[
                "statistics_test"
            ] = recommendation["test"]

            st.session_state[
                "analysis_completed"
            ] = True

            st.dataframe(result)

            # ==========================================
            # Post-hoc Analysis (Tukey HSD) for ANOVA
            # ==========================================

            if (
                recommendation["test"] == "ANOVA"
                and not result.empty
            ):

                try:

                    p_value = float(
                        result["p-unc"].iloc[0]
                    )

                    if p_value < 0.05:

                        st.subheader(
                            "Post-hoc Analysis (Tukey HSD)"
                        )

                        tukey_result = run_analysis(
                            df=df,
                            test_name="Tukey HSD",
                            group_col=group_col,
                            outcome_col=outcome_col
                        )

                        st.dataframe(
                            tukey_result
                        )

                except Exception:
                    pass

            report_text = generate_academic_report(
                recommendation["test"],
                result
            )

            st.session_state[
                "statistics_report"
            ] = report_text

            st.subheader(
                "Academic Report"
            )

            st.write(
                report_text
            )

    # =========================
    # Correlation Analysis
    # =========================

    elif analysis_type == "Correlation Analysis":

        variable_1 = st.selectbox(
            "Variable 1",
            report["numeric_columns"]
        )

        variable_2 = st.selectbox(
            "Variable 2",
            report["numeric_columns"]
        )

        correlation_type = st.selectbox(
            "Correlation Test",
            [
                "Pearson Correlation",
                "Spearman Correlation",
            ],
        )

        if st.button("Run Analysis"):

            result = run_analysis(
                df=df,
                test_name=correlation_type,
                variable_1=variable_1,
                variable_2=variable_2,
            )

            st.session_state[
                "statistics_results"
            ] = result

            st.session_state[
                "statistics_test"
            ] = correlation_type

            st.session_state[
                "analysis_completed"
            ] = True

            st.dataframe(result)

            report_text = generate_academic_report(
                correlation_type,
                result
            )

            st.session_state[
                "statistics_report"
            ] = report_text

            st.write(
                report_text
            )

    # =========================
    # Categorical Association
    # =========================

    elif analysis_type == "Categorical Association":

        variable_1 = st.selectbox(
            "Variable 1",
            report["categorical_columns"]
        )

        variable_2 = st.selectbox(
            "Variable 2",
            report["categorical_columns"]
        )

        test_name = st.selectbox(
            "Association Test",
            [
                "Chi-Square Test",
                "Fisher Exact Test"
            ]
        )

        if st.button("Run Analysis"):

            result = run_analysis(
                df=df,
                test_name=test_name,
                variable_1=variable_1,
                variable_2=variable_2,
            )

            st.session_state[
                "statistics_results"
            ] = result

            st.session_state[
                "statistics_test"
            ] = test_name

            st.session_state[
                "analysis_completed"
            ] = True

            st.write(result)

            report_text = generate_academic_report(
                test_name,
                result
            )

            st.session_state[
                "statistics_report"
            ] = report_text

            st.write(
                report_text
            )

    # =========================
    # Regression Analysis
    # =========================

    elif analysis_type == "Regression Analysis":

        from research_analytics.statsmodels_engine import (
            run_linear_regression,
            run_logistic_regression,
        )

        regression_type = st.selectbox(
            "Regression Type",
            [
                "Linear Regression",
                "Logistic Regression"
            ]
        )

        outcome_variable = st.selectbox(
            "Outcome Variable",
            report["numeric_columns"]
        )

        predictor_variables = st.multiselect(
            "Predictor Variables",
            [
                col
                for col in report["numeric_columns"]
                if col != outcome_variable
            ],
        )

        if st.button("Run Regression"):

            if not predictor_variables:

                st.warning(
                    "Please select at least one predictor."
                )

            else:

                if regression_type == "Linear Regression":

                    result = run_linear_regression(
                        df,
                        outcome_variable,
                        predictor_variables
                    )

                    st.metric(
                        "R²",
                        round(
                            result["r_squared"],
                            3
                        )
                    )

                else:

                    result = run_logistic_regression(
                        df,
                        outcome_variable,
                        predictor_variables
                    )

                    st.metric(
                        "Pseudo R²",
                        round(
                            result["pseudo_r_squared"],
                            3
                        )
                    )

                st.session_state[
                    "statistics_results"
                ] = result

                st.session_state[
                    "statistics_test"
                ] = regression_type

                st.session_state[
                    "analysis_completed"
                ] = True

                st.subheader(
                    "Model Results"
                )

                st.dataframe(
                    result["results"]
                )

                report_text = (
                    generate_academic_report(
                        regression_type,
                        result
                    )
                )

                st.session_state[
                    "statistics_report"
                ] = report_text

                st.subheader(
                    "Academic Report"
                )

                st.write(
                    report_text
                )

                with st.expander(
                    "Model Summary"
                ):

                    st.text(
                        result["summary"]
                    )
