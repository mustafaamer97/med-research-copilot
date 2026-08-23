import pingouin as pg
import pandas as pd


def run_ttest(df, group_col, outcome_col):

    if not pd.api.types.is_numeric_dtype(df[outcome_col]):
        raise ValueError("Outcome variable must be numeric.")

    groups = df[group_col].dropna().unique()

    if len(groups) != 2:
        raise ValueError("Independent t-test requires exactly 2 groups.")

    g1 = df[df[group_col] == groups[0]][outcome_col].dropna()
    g2 = df[df[group_col] == groups[1]][outcome_col].dropna()

    return pg.ttest(g1, g2, paired=False)


def run_mannwhitney(df, group_col, outcome_col):

    if not pd.api.types.is_numeric_dtype(df[outcome_col]):
        raise ValueError("Outcome variable must be numeric.")

    groups = df[group_col].dropna().unique()

    if len(groups) != 2:
        raise ValueError("Mann-Whitney requires exactly 2 groups.")

    g1 = df[df[group_col] == groups[0]][outcome_col].dropna()
    g2 = df[df[group_col] == groups[1]][outcome_col].dropna()

    return pg.mwu(g1, g2)


def run_anova(df, group_col, outcome_col):

    if not pd.api.types.is_numeric_dtype(df[outcome_col]):
        raise ValueError("Outcome variable must be numeric.")

    result = pg.anova(
        data=df,
        dv=outcome_col,
        between=group_col
    )

    return result


def run_pearson_correlation(
    df,
    variable_1,
    variable_2
):

    if not pd.api.types.is_numeric_dtype(
        df[variable_1]
    ):
        raise ValueError(
            f"{variable_1} must be numeric."
        )

    if not pd.api.types.is_numeric_dtype(
        df[variable_2]
    ):
        raise ValueError(
            f"{variable_2} must be numeric."
        )

    data = df[
        [variable_1, variable_2]
    ].dropna()

    result = pg.corr(
        data[variable_1],
        data[variable_2],
        method="pearson"
    )

    return result


def run_spearman_correlation(
    df,
    variable_1,
    variable_2
):

    if not pd.api.types.is_numeric_dtype(
        df[variable_1]
    ):
        raise ValueError(
            f"{variable_1} must be numeric."
        )

    if not pd.api.types.is_numeric_dtype(
        df[variable_2]
    ):
        raise ValueError(
            f"{variable_2} must be numeric."
        )

    data = df[
        [variable_1, variable_2]
    ].dropna()

    result = pg.corr(
        data[variable_1],
        data[variable_2],
        method="spearman"
    )

    return result


def run_analysis(
    df,
    test_name,
    group_col=None,
    outcome_col=None,
    variable_1=None,
    variable_2=None
):

    if test_name == "Independent t-test":

        return run_ttest(
            df,
            group_col,
            outcome_col
        )

    if test_name == "Mann-Whitney U Test":

        return run_mannwhitney(
            df,
            group_col,
            outcome_col
        )

    if test_name == "ANOVA":

        return run_anova(
            df,
            group_col,
            outcome_col
        )

    if test_name == "Pearson Correlation":

        return run_pearson_correlation(
            df,
            variable_1,
            variable_2
        )

    if test_name == "Spearman Correlation":

        return run_spearman_correlation(
            df,
            variable_1,
            variable_2
        )

    raise ValueError(
        f"Unsupported test: {test_name}"
    )
