import pandas as pd
import statsmodels.api as sm
import numpy as np


def run_linear_regression(
    df,
    outcome_variable,
    predictor_variables
):

    columns = predictor_variables + [
        outcome_variable
    ]

    data = df[
        columns
    ].dropna()

    X = data[
        predictor_variables
    ]

    y = data[
        outcome_variable
    ]

    X = sm.add_constant(X)

    model = sm.OLS(
        y,
        X
    ).fit()

    coefficients = pd.DataFrame(
        {
            "Variable": model.params.index,
            "Coefficient": model.params.values,
            "P-value": model.pvalues.values,
            "CI Lower": model.conf_int()[0].values,
            "CI Upper": model.conf_int()[1].values,
        }
    )

    return {
        "model_type": "Linear Regression",
        "r_squared": float(
            model.rsquared
        ),
        "adj_r_squared": float(
            model.rsquared_adj
        ),
        "results": coefficients,
        "summary": model.summary().as_text()
    }


def run_logistic_regression(
    df,
    outcome_variable,
    predictor_variables
):

    columns = predictor_variables + [
        outcome_variable
    ]

    data = df[
        columns
    ].dropna()

    X = data[
        predictor_variables
    ]

    y = data[
        outcome_variable
    ]

    X = sm.add_constant(X)

    model = sm.Logit(
        y,
        X
    ).fit(
        disp=False
    )

    odds_ratios = np.exp(
        model.params
    )

    conf_int = np.exp(
        model.conf_int()
    )

    results = pd.DataFrame(
        {
            "Variable": odds_ratios.index,
            "Odds Ratio": odds_ratios.values,
            "P-value": model.pvalues.values,
            "CI Lower": conf_int[0].values,
            "CI Upper": conf_int[1].values,
        }
    )

    return {
        "model_type": "Logistic Regression",
        "pseudo_r_squared": float(
            model.prsquared
        ),
        "results": results,
        "summary": model.summary().as_text()
    }
