import pingouin as pg


def run_ttest(
    data,
    group_column,
    outcome_column
):

    result = pg.ttest(
        x=data[data[group_column] == data[group_column].unique()[0]][outcome_column],
        y=data[data[group_column] == data[group_column].unique()[1]][outcome_column],
        paired=False
    )

    return result



def run_anova(
    data,
    group_column,
    outcome_column
):

    result = pg.anova(
        data=data,
        dv=outcome_column,
        between=group_column
    )

    return result



def run_chi_square(
    data,
    column1,
    column2
):

    result = pg.chi2_independence(
        data,
        x=column1,
        y=column2
    )

    return result
