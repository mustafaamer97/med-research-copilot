import pingouin as pg


def calculate_cohens_d(
    group1,
    group2
):

    effect = pg.compute_effsize(
        group1,
        group2,
        eftype="cohen"
    )

    return effect



def calculate_hedges_g(
    group1,
    group2
):

    effect = pg.compute_effsize(
        group1,
        group2,
        eftype="hedges"
    )

    return effect
