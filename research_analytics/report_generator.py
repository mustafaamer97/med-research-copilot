def generate_academic_report(
    test_name,
    result_df
):

    report = []

    report.append(
        f"Statistical Test: {test_name}"
    )

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

        # Cohen's d
        if "cohen-d" in result_df.columns:

            d = float(
                result_df["cohen-d"].iloc[0]
            )

            report.append(
                f"Cohen's d: {d:.3f}"
            )

            abs_d = abs(d)

            if abs_d < 0.2:

                interpretation = "negligible effect"

            elif abs_d < 0.5:

                interpretation = "small effect"

            elif abs_d < 0.8:

                interpretation = "moderate effect"

            else:

                interpretation = "large effect"

            report.append(
                f"Effect Size Interpretation: {interpretation}"
            )

            report.append(
                f"The observed effect size was {interpretation} (Cohen's d = {d:.3f})."
            )

    # ANOVA (في حال وجود p-unc)
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
