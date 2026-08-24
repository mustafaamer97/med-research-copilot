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

        pmid = str(
            article["MedlineCitation"]["PMID"]
        )

        pubmed_url = (
            f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        )

        doi = ""

        try:

            for item in article["PubmedData"]["ArticleIdList"]:

                if item.attributes.get("IdType") == "doi":

                    doi = str(item)
                    break

        except:
            pass

        authors = ""

        try:

            author_list = article[
                "MedlineCitation"
            ]["Article"]["AuthorList"]

            authors = ", ".join(
                [
                    f"{a.get('ForeName', '')} {a.get('LastName', '')}".strip()
                    for a in author_list
                    if "LastName" in a
                ]
            )

        except:
            pass

        journal = ""

        try:

            journal = str(
                article["MedlineCitation"]
                ["Article"]
                ["Journal"]
                ["Title"]
            )

        except:
            pass

        year = ""

        try:

            year = str(
                article["MedlineCitation"]
                ["Article"]
                ["Journal"]
                ["JournalIssue"]
                ["PubDate"]
                ["Year"]
            )

        except:
            pass

        papers.append(
            {
                "pmid": pmid,
                "title": str(title),
                "authors": authors,
                "journal": journal,
                "year": year,
                "doi": doi,
                "url": pubmed_url,
                "abstract": str(abstract)
            }
        )

    return papers
