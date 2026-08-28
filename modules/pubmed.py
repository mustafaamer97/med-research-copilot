import re
import os
from Bio import Entrez

from modules.evidence_classifier import (
    classify_evidence_level,
    evidence_score
)

# تعيين البريد الإلكتروني من المتغيرات البيئية أو القيمة الافتراضية
Entrez.email = os.getenv("ENTREZ_EMAIL", "mustafaamer97@gmail.com")


# =====================================
# Query Optimizer
# =====================================

def optimize_query(query):

    if not query:
        return ""

    query = query.lower()

    stop_words = [
        "adults",
        "adult",
        "children",
        "child",
        "patients",
        "patient",
        "population",
        "group",
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
        "does",
        "compared",
        "comparison",
        "improve",
        "improved"
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
        dict.fromkeys(
            keywords
        )
    )

    return " AND ".join(
        keywords[:10]
    )


# =====================================
# Animal Filter
# =====================================

def is_animal_study(article):

    try:

        mesh_terms = article[
            "MedlineCitation"
        ].get(
            "MeshHeadingList",
            []
        )

        for mesh in mesh_terms:

            name = str(
                mesh.get(
                    "DescriptorName",
                    ""
                )
            ).lower()

            if name in [
                "animals",
                "mice",
                "rats",
                "dogs",
                "cats"
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

    text = (
        publication_type.lower()
    )

    excluded = [
        "editorial",
        "letter",
        "comment",
        "news",
        "biography"
    ]

    return any(
        item in text
        for item in excluded
    )


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

    try:

        handle = Entrez.esearch(
            db="pubmed",
            term=optimized_query,
            retmax=max_results,
            sort="relevance"
        )

        results = Entrez.read(
            handle
        )

        ids = results[
            "IdList"
        ]

        if not ids:
            return []

        return get_details(
            ids
        )

    except Exception as e:

        print(
            f"PubMed Search Error: {e}"
        )

        return []


# =====================================
# Paper Details
# =====================================

def get_details(ids):

    papers = []

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
            f"PubMed Fetch Error: {e}"
        )

        return []

    for article in records[
        "PubmedArticle"
    ]:

        if is_animal_study(article):
            continue

        citation = article[
            "MedlineCitation"
        ]

        article_data = citation[
            "Article"
        ]

        title = str(
            article_data.get(
                "ArticleTitle",
                ""
            )
        )

        abstract = ""

        try:

            abstract = " ".join(
                [
                    str(x)
                    for x in article_data[
                        "Abstract"
                    ][
                        "AbstractText"
                    ]
                ]
            )

        except:
            pass

        pmid = str(
            citation[
                "PMID"
            ]
        )

        publication_type = ""

        try:

            publication_type = ", ".join(
                [
                    str(x)
                    for x in article_data[
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

        year = ""

        try:

            year = str(
                article_data[
                    "Journal"
                ][
                    "JournalIssue"
                ][
                    "PubDate"
                ].get(
                    "Year",
                    ""
                )
            )

        except:
            pass

        doi = ""

        try:

            for item in article[
                "PubmedData"
            ][
                "ArticleIdList"
            ]:

                if item.attributes.get(
                    "IdType"
                ) == "doi":

                    doi = str(
                        item
                    )

                    break

        except:
            pass

        # =====================================
        # التعديل الجديد: بناء full_text والتصنيف
        # =====================================
        full_text = f"""
{title}

{abstract}

{publication_type}
"""

        evidence_level = classify_evidence_level(
            full_text
        )

        evidence_score_value = evidence_score(
            evidence_level
        )

        papers.append(
            {
                "pmid":
                pmid,

                "title":
                title,

                "authors":
                "",

                "journal":
                str(
                    article_data[
                        "Journal"
                    ][
                        "Title"
                    ]
                ),

                "year":
                year,

                "doi":
                doi,

                "url":
                f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",

                "publication_type":
                publication_type,

                "evidence_level":
                evidence_level,

                "evidence_score":
                evidence_score_value,

                "abstract":
                abstract,

                "source":
                "PubMed",

                "citation_count":
                0
            }
        )

    return papers
