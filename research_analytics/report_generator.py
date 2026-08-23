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
        d = None
        interpretation = "unknown effect"

        if "cohen-d" in result_df.columns:

            d = float(
                result_df["cohen-d"].iloc[0]
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
                f"Cohen's d: {d:.3f}"
            )

            report.append(
                f"Effect Size Interpretation: {interpretation}"
            )

        # 95% Confidence Interval
        if "CI95%" in result_df.columns:

            ci = result_df["CI95%"].iloc[0]

            report.append(
                f"95% Confidence Interval: {ci}"
            )

        # Statistical Power
        if "power" in result_df.columns:

            power = float(
                result_df["power"].iloc[0]
            )

            report.append(
                f"Statistical Power: {power:.3f}"
            )

            if power >= 0.80:

                report.append(
                    "The study appears adequately powered."
                )

            else:

                report.append(
                    "The statistical power may be insufficient."
                )

        # Publication-Ready Paragraph
        if d is not None:
            if p_value < 0.05:
                report.append(
                    f"An independent samples t-test demonstrated "
                    f"a statistically significant difference "
                    f"between groups (p = {p_value:.3f}). "
                    f"The effect size was {interpretation} "
                    f"(Cohen's d = {d:.2f})."
                )
            else:
                report.append(
                    f"An independent samples t-test showed "
                    f"no statistically significant difference "
                    f"between groups (p = {p_value:.3f}). "
                    f"The effect size was {interpretation} "
                    f"(Cohen's d = {d:.2f})."
                )

    return "\n\n".join(report)
