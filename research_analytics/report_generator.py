def generate_academic_report(
    test_name,
    result_df
):

    report = []

    report.append(
        f"Statistical Test: {test_name}"
    )

    # t-test
    if "p-val" in result_df.columns:

        p_value = float(
            result_df["p-val"].iloc[0]
        )

        report.append(
            f"P-value: {p_value:.4f}"
        )

        if p_value < 0.05:

            report.append(
                "There was a statistically significant difference between the groups."
            )

        else:

            report.append(
                "No statistically significant difference was observed between the groups."
            )

    # ANOVA
    elif "p-unc" in result_df.columns:

        p_value = float(
            result_df["p-unc"].iloc[0]
        )

        report.append(
            f"P-value: {p_value:.4f}"
        )

        if p_value < 0.05:

            report.append(
                "A statistically significant difference was found among the groups."
            )

        else:

            report.append(
                "No statistically significant difference was found among the groups."
            )

    return "\n\n".join(report)
