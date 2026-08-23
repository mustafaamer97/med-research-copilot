def suggest_test(
    variable_type,
    groups,
    objective
):

    # مقارنة متوسط بين مجموعتين

    if (
        variable_type == "continuous"
        and groups == 2
        and objective == "comparison"
    ):

        return {
            "test": "Independent t-test",
            "alternative": "Mann-Whitney U test",
            "reason":
            "Continuous outcome with two independent groups"
        }


    # مقارنة أكثر من مجموعتين

    if (
        variable_type == "continuous"
        and groups > 2
        and objective == "comparison"
    ):

        return {
            "test": "ANOVA",
            "alternative": "Kruskal-Wallis test",
            "reason":
            "Continuous outcome with multiple groups"
        }


    # علاقة بين متغيرين

    if (
        variable_type == "continuous"
        and objective == "correlation"
    ):

        return {
            "test": "Pearson correlation",
            "alternative": "Spearman correlation",
            "reason":
            "Assess relationship between variables"
        }


    # متغيرات فئوية

    if (
        variable_type == "categorical"
        and objective == "comparison"
    ):

        return {
            "test": "Chi-square test",
            "alternative": "Fisher exact test",
            "reason":
            "Comparison between categorical variables"
        }


    return {
        "test": "Need more information",
        "reason":
        "Study design or variable information is incomplete"
    }
