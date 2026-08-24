def auto_select_group_comparison_test(
    df,
    report,
    group_col,
    outcome_col
):

    # التأكد أن المتغير الناتج رقمي

    if outcome_col not in report["numeric_columns"]:

        return {
            "test": None,
            "reason":
            "Outcome variable must be numeric."
        }

    # عدد المجموعات

    groups = (
        df[group_col]
        .dropna()
        .nunique()
    )

    # الطبيعية

    normal = True

    if outcome_col in report["normality"]:

        normal = report["normality"][
            outcome_col
        ]["normal"]

    # مجموعتان

    if groups == 2:

        if normal:

            return {
                "test":
                "Independent t-test",

                "reason":
                "Two groups with normal distribution."
            }

        return {
            "test":
            "Mann-Whitney U Test",

            "reason":
            "Two groups with non-normal distribution."
        }

    # أكثر من مجموعتين

    if groups > 2:

        if normal:

            return {
                "test":
                "ANOVA",

                "reason":
                "Multiple groups with normal distribution."
            }

        return {
            "test":
            "Kruskal-Wallis",

            "reason":
            "Multiple groups with non-normal distribution."
        }

    return {
        "test": None,
        "reason":
        "Unable to determine appropriate test."
    }
