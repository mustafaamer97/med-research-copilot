from statsmodels.stats.power import (
    TTestIndPower,
    NormalIndPower
)


def calculate_sample_size(
    study_type,
    effect_size,
    alpha=0.05,
    power=0.80
):

    study_type = str(
        study_type
    ).lower()

    # ==================================
    # RCT
    # ==================================

    if "rct" in study_type:

        analysis = TTestIndPower()

        n = analysis.solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power,
            alternative="two-sided"
        )

        return int(round(n))

    # ==================================
    # Cohort
    # ==================================

    elif "cohort" in study_type:

        analysis = NormalIndPower()

        n = analysis.solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power
        )

        return int(round(n))

    # ==================================
    # Case-Control
    # ==================================

    elif "case-control" in study_type:

        analysis = NormalIndPower()

        n = analysis.solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power
        )

        return int(round(n))

    # ==================================
    # Cross-Sectional
    # ==================================

    elif "cross-sectional" in study_type:

        analysis = NormalIndPower()

        n = analysis.solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power
        )

        return int(round(n))

    # ==================================
    # Default
    # ==================================

    analysis = TTestIndPower()

    n = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power
    )

    return int(round(n))
