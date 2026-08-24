from Bio import Entrez

Entrez.email = "your_email@example.com"


def is_animal_study(article):
    try:
        mesh_terms = article["MedlineCitation"]["MeshHeadingList"]

        for mesh in mesh_terms:
            if str(mesh["DescriptorName"]).lower() in [
                "mice",
                "rats",
                "animals",
                "cats",
                "dogs"
            ]:
                return True

    except:
        pass

    return False


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

        # استبعاد الدراسات الحيوانية
        if is_animal_study(article):
            continue

        title = article["MedlineCitation"]["Article"]["ArticleTitle"]

        abstract = ""

        try:
            abstract_parts = article[
                "MedlineCitation"
            ]["Article"]["Abstract"]["AbstractText"]

            abstract = " ".join(
                [str(part) for part in abstract_parts]
            )

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

        publication_date = ""

        try:
            pub_date = article[
                "MedlineCitation"
            ]["Article"]["Journal"]["JournalIssue"]["PubDate"]

            publication_date = " ".join(
                [str(v) for v in pub_date.values()]
            )

        except:
            pass

        publication_type = ""

        try:
            publication_types = article[
                "MedlineCitation"
            ]["Article"]["PublicationTypeList"]

            publication_type = ", ".join(
                [str(p) for p in publication_types]
            )

        except:
            pass

        mesh_terms = ""

        try:
            mesh_list = article[
                "MedlineCitation"
            ]["MeshHeadingList"]

            mesh_terms = ", ".join(
                [
                    str(mesh["DescriptorName"])
                    for mesh in mesh_list
                ]
            )

        except:
            pass

        language = ""

        try:
            language = ", ".join(
                article["MedlineCitation"]
                ["Article"]
                ["Language"]
            )

        except:
            pass

        country = ""

        try:
            country = str(
                article["MedlineCitation"]
                ["MedlineJournalInfo"]
                ["Country"]
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
                "publication_date": publication_date,
                "doi": doi,
                "url": pubmed_url,
                "publication_type": publication_type,
                "mesh_terms": mesh_terms,
                "language": language,
                "country": country,
                "abstract": str(abstract)
            }
        )

    return papers
