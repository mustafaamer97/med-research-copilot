import pingouin as pg


def run_independent_ttest(
    data,
    group,
    outcome
):

    groups = data[group].unique()

    result = pg.ttest(
        data[data[group] == groups[0]][outcome],
        data[data[group] == groups[1]][outcome]
    )

    return result
