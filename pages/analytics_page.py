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
from modules.context_manager import (
    update_context,
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

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", report["rows"])
        st.metric("Columns", report["columns"])

    with col2:
        st.metric("Duplicates", report["duplicates"])
        st.metric(
            "Numeric Variables",
            len(report.get("numeric_columns", []))
        )

    # 9. Dataset Quality Score
    quality_score = 100
    quality_score -= min(report.get("duplicates", 0), 20)
    missing_pct = report.get("missing_percentage", 0)
    quality_score -= min(int(missing_pct), 30)

    with col3:
        st.metric(
            "Dataset Quality",
            f"{max(0, quality_score)}%"
        )

    # 7. Missing Data Summary
    st.subheader("Missing Data Summary")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric(
            "Missing Values",
            report.get("missing_values", 0)
        )
    with col_m2:
        st.metric(
            "Missing Percentage",
            f"{report.get('missing_percentage', 0):.2f}%"
        )

    # 8. Normality Summary
    if report.get("normality"):
        st.subheader("Normality Check")
        st.json(report["normality"])

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

        # 1. Protection against missing numeric variables
        if not report.get("numeric_columns"):
            st.error("No numeric variables detected in the dataset.")
            return

        group_col = st.selectbox(
            "Grouping Variable",
            df.columns
        )

        outcome_col = st.selectbox(
            "Outcome Variable",
            report["numeric_columns"]
        )

        if st.button("Run Analysis"):

            recommendation = auto_select_group_comparison_test(
                df,
                report,
                group_col,
                outcome_col
            )

            # 3. Display complete Smart Selector recommendations
            st.info(f"Recommended Test: {recommendation['test']}")

            if recommendation.get("reason"):
                st.write(f"**Reason:** {recommendation['reason']}")

            if recommendation.get("effect_size"):
                st.write(f"**Effect Size:** {recommendation['effect_size']}")

            if recommendation.get("posthoc"):
                st.write(f"**Post-hoc:** {recommendation['posthoc']}")

            if recommendation.get("warning"):
                st.warning(recommendation["warning"])

            result = run_analysis(
                df=df,
                test_name=recommendation["test"],
                group_col=group_col,
                outcome_col=outcome_col,
            )

            st.dataframe(result)

            # Post-hoc Analysis (Tukey HSD) for ANOVA
            if recommendation["test"] == "ANOVA" and not result.empty:
                try:
                    p_value = float(result["p-unc"].iloc[0])
                    if p_value < 0.05:
                        st.subheader("Post-hoc Analysis (Tukey HSD)")
                        tukey_result = run_analysis(
                            df=df,
                            test_name="Tukey HSD",
                            group_col=group_col,
                            outcome_col=outcome_col
                        )
                        st.dataframe(tukey_result)
                except Exception:
                    pass

            report_text = generate_academic_report(
                recommendation["test"],
                result
            )

            # 4 & 5. Save Analysis into Context Manager
            update_context(
                statistics_results=result,
                statistics_test=recommendation["test"],
                statistics_report=report_text,
                selected_effect_size=recommendation.get("effect_size"),
                analysis_completed=True
            )

            st.subheader("Academic Report")
            st.write(report_text)

    # =========================
    # Correlation Analysis
    # =========================

    elif analysis_type == "Correlation Analysis":

        # Protection against missing numeric variables
        if not report.get("numeric_columns"):
            st.error("No numeric variables detected in the dataset.")
            return

        variable_1 = st.selectbox(
            "Variable 1",
            report["numeric_columns"]
        )

        variable_2 = st.selectbox(
            "Variable 2",
            report["numeric_columns"]
        )

        # 6. Prevent selecting the same variable twice
        if variable_1 == variable_2:
            st.warning("Please select two different variables.")
            return

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

            st.dataframe(result)

            report_text = generate_academic_report(
                correlation_type,
                result
            )

            # Save to Context
            update_context(
                statistics_results=result,
                statistics_test=correlation_type,
                statistics_report=report_text,
                analysis_completed=True
            )

            st.subheader("Academic Report")
            st.write(report_text)

    # =========================
    # Categorical Association
    # =========================

    elif analysis_type == "Categorical Association":

        # 2. Protection against missing categorical variables
        if not report.get("categorical_columns"):
            st.error("No categorical variables detected in the dataset.")
            return

        variable_1 = st.selectbox(
            "Variable 1",
            report["categorical_columns"]
        )

        variable_2 = st.selectbox(
            "Variable 2",
            report["categorical_columns"]
        )

        # Prevent selecting the same variable twice
        if variable_1 == variable_2:
            st.warning("Please select two different variables.")
            return

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

            st.write(result)

            report_text = generate_academic_report(
                test_name,
                result
            )

            # Save to Context
            update_context(
                statistics_results=result,
                statistics_test=test_name,
                statistics_report=report_text,
                analysis_completed=True
            )

            st.subheader("Academic Report")
            st.write(report_text)

    # =========================
    # Regression Analysis
    # =========================

    elif analysis_type == "Regression Analysis":

        # Protection against missing numeric variables
        if not report.get("numeric_columns"):
            st.error("No numeric variables detected in the dataset.")
            return

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
                st.warning("Please select at least one predictor.")
            else:
                if regression_type == "Linear Regression":
                    result = run_linear_regression(
                        df,
                        outcome_variable,
                        predictor_variables
                    )
                    st.metric(
                        "R²",
                        round(result["r_squared"], 3)
                    )
                else:
                    result = run_logistic_regression(
                        df,
                        outcome_variable,
                        predictor_variables
                    )
                    st.metric(
                        "Pseudo R²",
                        round(result["pseudo_r_squared"], 3)
                    )

                st.subheader("Model Results")
                st.dataframe(result["results"])

                report_text = generate_academic_report(
                    regression_type,
                    result
                )

                # Save to Context
                update_context(
                    statistics_results=result,
                    statistics_test=regression_type,
                    statistics_report=report_text,
                    analysis_completed=True
                )

                st.subheader("Academic Report")
                st.write(report_text)

                with st.expander("Model Summary"):
                    st.text(result["summary"])
