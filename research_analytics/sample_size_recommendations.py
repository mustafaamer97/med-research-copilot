def get_default_effect_size(
    study_type
):

    study_type = study_type.lower()

    if "rct" in study_type:
        return 0.5

    if "cohort" in study_type:
        return 0.3

    if "case-control" in study_type:
        return 0.3

    if "cross-sectional" in study_type:
        return 0.2

    return 0.5
