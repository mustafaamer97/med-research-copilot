def generate_pubmed_query(
    population,
    intervention,
    comparison,
    outcome
):

    query = f"""
    (
    {population}
    )
    AND
    (
    {intervention}
    )
    AND
    (
    {comparison}
    )
    AND
    (
    {outcome}
    )
    """

    return query.strip()
