from modules.pubmed import search_pubmed


PRIORITY_FILTERS = [

    "systematic review",

    "meta-analysis",

    "randomized controlled trial",

    "clinical trial",

    "cohort study",

    "observational study"

]



def get_recent_evidence(
    topic,
    max_results=20
):

    all_papers = []


    # ==================================
    # Search Multiple Evidence Types
    # ==================================

    per_filter_limit = max(
        5,
        max_results // len(PRIORITY_FILTERS)
    )


    for study_type in PRIORITY_FILTERS:


        query = (
            f"{topic} AND {study_type}"
        )


        try:

            papers = search_pubmed(
                query,
                max_results=per_filter_limit
            )


            all_papers.extend(
                papers
            )


        except Exception as e:


            print(
                f"Evidence search error ({study_type}): {e}"
            )



    # ==================================
    # Remove Duplicate Papers
    # ==================================

    unique_papers = {}



    for paper in all_papers:


        key = (

            paper.get("pmid")

            or

            paper.get("doi")

            or

            paper.get("title")

        )


        if key:

            unique_papers[key] = paper



    papers = list(
        unique_papers.values()
    )



    # ==================================
    # Evidence Ranking
    # ==================================

    ranking = {

        "Level 1": 1,

        "Level 2": 2,

        "Level 3": 3,

        "Level 4": 4,

        "Level 5": 5,

        "Unknown": 99

    }



    papers.sort(

        key=lambda paper:

        ranking.get(

            paper.get(
                "evidence_level",
                "Unknown"
            ),

            99

        )

    )



    return papers[:max_results]
