import pandas as pd

from statsmodels.stats.power import (
    TTestIndPower
)


def build_power_curve(
    effect_size,
    alpha=0.05
):

    analysis = TTestIndPower()

    rows = []

    for power in [
        0.60,
        0.70,
        0.80,
        0.90,
        0.95
    ]:

        n = analysis.solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power
        )

        rows.append(
            {
                "Power": power,
                "Sample Size": round(n)
            }
        )

    return pd.DataFrame(rows)
