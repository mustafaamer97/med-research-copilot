# modules/validators.py

import pandas as pd


DICHOTOMOUS_COLUMNS = [
    "study",
    "a",
    "b",
    "c",
    "d",
]

CONTINUOUS_COLUMNS = [
    "study",
    "n_t",
    "mean_t",
    "sd_t",
    "n_c",
    "mean_c",
    "sd_c",
]


def validate_dichotomous_data(df: pd.DataFrame) -> None:
    missing = set(DICHOTOMOUS_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {', '.join(missing)}"
        )

    if (df[["a", "b", "c", "d"]] < 0).any().any():
        raise ValueError(
            "Counts cannot be negative."
        )


def validate_continuous_data(df: pd.DataFrame) -> None:
    missing = set(CONTINUOUS_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {', '.join(missing)}"
        )

    numeric_cols = [
        "n_t",
        "mean_t",
        "sd_t",
        "n_c",
        "mean_c",
        "sd_c",
    ]

    if (df[numeric_cols] < 0).any().any():
        raise ValueError(
            "Values cannot be negative."
        )
