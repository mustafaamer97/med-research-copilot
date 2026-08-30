from statsmodels.stats.power import (
    TTestIndPower
)


def calculate_sample_size(
    effect_size,
    alpha=0.05,
    power=0.80,
    ratio=1.0
):

    analysis = TTestIndPower()

    sample_size = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative="two-sided"
    )

    return int(round(sample_size))


def classify_sample_size(
    total_n
):

    if total_n < 100:
        return "Small"

    if total_n < 500:
        return "Moderate"

    return "Large"
