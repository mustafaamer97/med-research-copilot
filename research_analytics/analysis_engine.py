import pingouin as pg
import pandas as pd


def run_ttest(df, group_col, outcome_col):

    if not pd.api.types.is_numeric_dtype(
        df[outcome_col]
    ):
        raise ValueError(
            "Outcome variable must be numeric."
        )

    groups = df[group_col].dropna().unique()

    if len(groups) != 2:
        raise ValueError(
            "Independent t-test requires exactly 2 groups."
        )

    g1 = df[
        df[group_col] == groups[0]
    ][outcome_col].dropna()

    g2 = df[
        df[group_col] == groups[1]
    ][outcome_col].dropna()

    return pg.ttest(
        g1,
        g2,
        paired=False
    )


def run_mannwhitney(df, group_col, outcome_col):

    if not pd.api.types.is_numeric_dtype(
        df[outcome_col]
    ):
        raise ValueError(
            "Outcome variable must be numeric."
        )

    groups = df[group_col].dropna().unique()

    if len(groups) != 2:
        raise ValueError(
            "Mann-Whitney requires exactly 2 groups."
        )

    g1 = df[
        df[group_col] == groups[0]
    ][outcome_col].dropna()

    g2 = df[
        df[group_col] == groups[1]
    ][outcome_col].dropna()

    return pg.mwu(
        g1,
        g2
    )


def run_analysis(
    df,
    test_name,
    group_col,
    outcome_col
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

    raise ValueError(
        f"Unsupported test: {test_name}"
    )
