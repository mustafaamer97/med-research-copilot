from Bio import Entrez
import re

from modules.evidence_classifier import (
    classify_evidence_level
)

Entrez.email = "mustafaamer97@gmail.com"


# =====================================
# Query Optimizer
# =====================================

def optimize_query(query):

    query = query.lower()

    stop_words = [
        "adults",
        "adult",
        "children",
        "patients",
        "population",
        "reduction",
        "improve",
        "improves",
        "improved",
        "compared",
        "comparison",
        "study",
        "trial",
        "effect",
        "outcome",
        "outcomes",
        "with",
        "and",
        "the",
        "of",
        "in",
        "on",
        "does"
    ]

    words = re.findall(
        r"[a-zA-Z0-9\-]+",
        query
    )

    keywords = []

    for word in words:

        if len(word) < 3:
            continue

        if word in stop_words:
            continue

        keywords.append(word)

    keywords = list(
        dict.fromkeys(keywords)
    )

    return " AND ".join(
        keywords[:8]
    )


# =====================================
# Animal Filter
# =====================================

def is_animal_study(article):

    try:

        mesh_terms = article[
            "MedlineCitation"
        ]["MeshHeadingList"]

        for mesh in mesh_terms:

            if str(
                mesh["DescriptorName"]
            ).lower() in [
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


# =====================================
# Low Evidence Filter
# =====================================

def is_low_evidence_study(
    publication_type
):

    publication_type = (
        publication_type.lower()
    )

    excluded_types = [
        "editorial",
        "letter",
        "comment",
        "news",
        "interview",
        "biography"
    ]

    for item in excluded_types:

        if item in publication_type:
            return True

    return False


# =====================================
# PubMed Search
# =====================================

def search_pubmed(
    query,
    max_results=10
):

    optimized_query = optimize_query(
        query
    )

    print(
        "\nOriginal Query:",
        query
    )

    print(
        "\nOptimized Query:",
        optimized_query
    )

    try:

        handle = Entrez.esearch(
            db="pubmed",
            term=optimized_query,
            retmax=max_results,
            sort="relevance"
        )

        results = Entrez.read(handle)

        ids = results["IdList"]

        print(
            "PubMed IDs:",
            ids
        )

        if not ids:
            return []

        return get_details(ids)

    except Exception as e:

        print(
            "PubMed Search Error:",
            e
        )

        return []


# =====================================
# Paper Details
# =====================================

def get_details(ids):

    try:

        handle = Entrez.efetch(
            db="pubmed",
            id=",".join(ids),
            rettype="medline",
            retmode="xml"
        )

        records = Entrez.read(
            handle
        )

    except Exception as e:

        print(
            "PubMed Fetch Error:",
            e
        )

        return []

    papers = []

    for article in records[
        "PubmedArticle"
    ]:

        if is_animal_study(article):
            continue

        title = ""

        try:
            title = str(
                article[
                    "MedlineCitation"
                ]["Article"][
                    "ArticleTitle"
                ]
            )
        except:
            pass

        abstract = ""

        try:

            abstract_parts = article[
                "MedlineCitation"
            ]["Article"][
                "Abstract"
            ]["AbstractText"]

            abstract = " ".join(
                [
                    str(part)
                    for part in abstract_parts
                ]
            )

        except:
            pass

        pmid = str(
            article[
                "MedlineCitation"
            ]["PMID"]
        )

        pubmed_url = (
            f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        )

        doi = ""

        try:

            for item in article[
                "PubmedData"
            ]["ArticleIdList"]:

                if (
                    item.attributes.get(
                        "IdType"
                    )
                    == "doi"
                ):
                    doi = str(item)
                    break

        except:
            pass

        authors = ""

        try:

            author_list = article[
                "MedlineCitation"
            ]["Article"][
                "AuthorList"
            ]

            authors = ", ".join(
                [
                    f"{a.get('ForeName','')} {a.get('LastName','')}".strip()
                    for a in author_list
                    if "LastName" in a
                ]
            )

        except:
            pass

        journal = ""

        try:

            journal = str(
                article[
                    "MedlineCitation"
                ]["Article"][
                    "Journal"
                ]["Title"]
            )

        except:
            pass

        year = ""

        try:

            year = str(
                article[
                    "MedlineCitation"
                ]["Article"][
                    "Journal"
                ]["JournalIssue"][
                    "PubDate"
                ]["Year"]
            )

        except:
            pass

        publication_type = ""

        try:

            publication_type = ", ".join(
                [
                    str(p)
                    for p in article[
                        "MedlineCitation"
                    ]["Article"][
                        "PublicationTypeList"
                    ]
                ]
            )

        except:
            pass

        if is_low_evidence_study(
            publication_type
        ):
            continue

        evidence_level = (
            classify_evidence_level(
                publication_type
            )
        )

        papers.append(
            {
                "pmid": pmid,
                "title": title,
                "authors": authors,
                "journal": journal,
                "year": year,
                "doi": doi,
                "url": pubmed_url,
                "publication_type": publication_type,
                "evidence_level": evidence_level,
                "abstract": abstract
            }
        )

    return papers
