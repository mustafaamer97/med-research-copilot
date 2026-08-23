from Bio import Entrez


Entrez.email = "your_email@example.com"


def search_pubmed(query, max_results=10):

    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results
    )

    results = Entrez.read(handle)

    ids = results["IdList"]

    if not ids:
        return []

    papers = get_details(ids)

    return papers



def get_details(ids):

    handle = Entrez.efetch(
        db="pubmed",
        id=",".join(ids),
        rettype="medline",
        retmode="xml"
    )

    records = Entrez.read(handle)

    papers = []

    for article in records["PubmedArticle"]:

        title = article["MedlineCitation"]["Article"]["ArticleTitle"]

        abstract = ""

        try:
            abstract = article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]
        except:
            pass


        papers.append(
            {
                "title": str(title),
                "abstract": str(abstract)
            }
        )

    return papers
