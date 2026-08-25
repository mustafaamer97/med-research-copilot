from statsmodels.stats.power import TTestIndPower


def calculate_sample_size(
    effect_size,
    alpha=0.05,
    power=0.80
):

    analysis = TTestIndPower()

    sample_size = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        alternative="two-sided"
    )

    return int(round(sample_size))
