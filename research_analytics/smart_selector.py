def suggest_test(
    outcome_type,
    groups,
    objective="comparison",
    paired=False,
    normal_distribution=True
):

    # مقارنة بين مجموعتين

    if (
        objective == "comparison"
        and outcome_type == "continuous"
        and groups == 2
    ):

        if paired:

            return {
                "test": "Paired t-test"
                if normal_distribution
                else "Wilcoxon Signed-Rank Test",

                "reason":
                "Paired continuous measurements.",

                "engine": "pingouin"
            }

        return {
            "test": "Independent t-test"
            if normal_distribution
            else "Mann-Whitney U Test",

            "reason":
            "Comparison of two independent groups.",

            "engine": "pingouin"
        }

    # أكثر من مجموعتين

    if (
        objective == "comparison"
        and outcome_type == "continuous"
        and groups > 2
    ):

        return {
            "test": "ANOVA"
            if normal_distribution
            else "Kruskal-Wallis",

            "reason":
            "Comparison among multiple groups.",

            "engine": "pingouin"
        }

    # متغيرات فئوية

    if outcome_type == "categorical":

        return {
            "test": "Chi-Square Test",

            "reason":
            "Association between categorical variables.",

            "engine": "pingouin",

            "alternative":
            "Fisher Exact Test"
        }

    # ارتباط

    if objective == "correlation":

        return {
            "test": "Pearson Correlation"
            if normal_distribution
            else "Spearman Correlation",

            "reason":
            "Relationship between variables.",

            "engine": "pingouin"
        }

    return {
        "test": "More information required",
        "reason": "Unable to determine test."
    }
