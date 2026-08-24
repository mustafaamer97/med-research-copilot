from modules.pubmed import search_pubmed


def get_recent_evidence(topic):

    papers = search_pubmed(
        topic,
        max_results=5
    )

    return papers
