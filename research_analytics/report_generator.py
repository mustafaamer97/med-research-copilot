import pandas as pd


def generate_academic_report(
    test_name,
    result_df
):

    report = []

    report.append(
        f"Statistical Test: {test_name}"
    )

    # Fisher Exact Test
    if test_name == "Fisher Exact Test":

        p_value = float(
            result_df["p_value"]
        )

        odds_ratio = float(
            result_df["odds_ratio"]
        )

        report.append(
            f"Odds Ratio: {odds_ratio:.3f}"
        )

        report.append(
            f"P-value: {p_value:.4f}"
        )

        if p_value < 0.05:

            report.append(
                "A statistically significant association was observed between the variables."
            )

        else:

            report.append(
                "No statistically significant association was observed between the variables."
            )

        # Publication-Ready Paragraph
        report.append(
            f"Fisher's Exact Test showed "
            f"{'a statistically significant' if p_value < 0.05 else 'no statistically significant'} "
            f"association between the variables "
            f"(OR = {odds_ratio:.2f}, p = {p_value:.3f})."
        )

    # Chi-Square Test
    elif test_name == "Chi-Square Test":

        chi_row = result_df[
            result_df["test"] == "pearson"
        ].iloc[0]

        chi2 = float(
            chi_row["chi2"]
        )

        p_value = float(
            chi_row["pval"]
        )

        report.append(
            f"Chi-Square Statistic: {chi2:.3f}"
        )

        report.append(
            f"P-value: {p_value:.4f}"
        )

        if p_value < 0.05:

            report.append(
                "A statistically significant association was found between the categorical variables."
            )

        else:

            report.append(
                "No statistically significant association was found between the categorical variables."
            )

        # Publication-Ready Paragraph
        report.append(
            f"A Chi-Square test of independence "
            f"{'demonstrated' if p_value < 0.05 else 'did not demonstrate'} "
            f"a significant association between the variables "
            f"(χ² = {chi2:.2f}, p = {p_value:.3f})."
        )

    # Correlation Analysis (r)
    elif isinstance(result_df, pd.DataFrame) and "r" in result_df.columns:

        r = float(
            result_df["r"].iloc[0]
        )

        p_value = float(
            result_df["p-val"].iloc[0]
        )

        report.append(
            f"Correlation coefficient (r): {r:.3f}"
        )

        report.append(
            f"P-value: {p_value:.4f}"
        )

        abs_r = abs(r)

        if abs_r < 0.30:
            strength = "weak"
        elif abs_r < 0.50:
            strength = "moderate"
        else:
            strength = "strong"

        direction = (
            "positive"
            if r > 0
            else "negative"
        )

        report.append(
            f"A {strength} {direction} correlation was observed."
        )

        if p_value < 0.05:
            report.append(
                f"The correlation between the variables was statistically significant (r = {r:.3f}, p = {p_value:.3f})."
            )
        else:
            report.append(
                f"No statistically significant correlation was observed between the variables (r = {r:.3f}, p = {p_value:.3f})."
            )

    # Group Comparisons (t-test / Mann-Whitney)
    elif isinstance(result_df, pd.DataFrame) and "p-val" in result_df.columns:

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
