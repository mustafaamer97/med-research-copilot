def select_test(
    outcome_type,
    predictor_type,
    groups,
    paired=False,
    objective="comparison"
):

    # مقارنة متغير مستمر بين مجموعتين

    if (
        objective == "comparison"
        and outcome_type == "continuous"
        and groups == 2
        and paired == False
    ):

        return {
            "test": "Independent t-test",
            "engine": "pingouin",
            "alternative": "Mann-Whitney U",
            "explanation":
            "Compare means between two independent groups."
        }


    # قبل وبعد لنفس المرضى

    if (
        objective == "comparison"
        and outcome_type == "continuous"
        and paired == True
    ):

        return {
            "test": "Paired t-test",
            "engine": "pingouin",
            "alternative":
            "Wilcoxon signed-rank test",
            "explanation":
            "Compare measurements before and after intervention."
        }


    # أكثر من مجموعتين

    if (
        outcome_type == "continuous"
        and groups > 2
    ):

        return {
            "test": "ANOVA",
            "engine": "pingouin",
            "alternative":
            "Kruskal-Wallis",
            "explanation":
            "Compare continuous outcome among multiple groups."
        }


    # متغيرات فئوية

    if (
        outcome_type == "categorical"
    ):

        return {
            "test": "Chi-square",
            "engine": "pingouin",
            "alternative":
            "Fisher Exact Test",
            "explanation":
            "Analyze association between categorical variables."
        }


    return {
        "test": "More information needed",
        "explanation":
        "The study design is not clear."
    }
