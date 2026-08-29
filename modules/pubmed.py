import re
from Bio import Entrez
import streamlit as st
from modules.evidence_classifier import classify_evidence_level

Entrez.email = "mustafaamer97@gmail.com"


# =====================================
# Query Optimizer
# =====================================

def optimize_query(query: str) -> str:
    if not query:
        return ""

    query = query.lower()

    stop_words = [
        "adults", "adult", "children", "child", "patients", "patient",
        "population", "group", "study", "trial", "effect", "outcome",
        "outcomes", "with", "and", "the", "of", "in", "on", "does",
        "compared", "comparison", "improve", "improved"
    ]

    words = re.findall(r"[a-zA-Z0-9\-]+", query)

    keywords = []
    for word in words:
        if len(word) < 3 or word in stop_words:
            continue
        keywords.append(word)

    # حفظ الكلمات الفريدة مع الحفاظ على الترتيب
    keywords = list(dict.fromkeys(keywords))

    return " AND ".join(keywords[:10])


# =====================================
# Animal Filter (Smart Check)
# =====================================

def is_animal_study(article: dict) -> bool:
    """
    يتحقق مما إذا كانت الدراسة على الحيوانات فقط.
    إذا كانت الدراسة تحتوي على Humans و Animals معاً، لا تعتبر دراسة حيوانية فقط.
    """
    try:
        mesh_terms = article["MedlineCitation"].get("MeshHeadingList", [])
        
        has_animals = False
        has_humans = False

        animal_keywords = ["animals", "mice", "rats", "dogs", "cats", "rabbits", "swine"]

        for mesh in mesh_terms:
            name = str(mesh.get("DescriptorName", "")).lower()

            if any(k in name for k in animal_keywords):
                has_animals = True
            elif "humans" in name:
                has_humans = True

        # يستبعد الدراسة فقط إذا كانت حيوانية ولم تذكر البشر
        if has_animals and not has_humans:
            return True

    except Exception:
        pass

    return False


# =====================================
# Low Evidence Filter
# =====================================

def is_low_evidence_study(publication_type: str) -> bool:
    text = publication_type.lower()
    excluded = ["editorial", "letter", "comment", "news", "biography"]
    return any(item in text for item in excluded)


# =====================================
# PubMed Search (Cached)
# =====================================

@st.cache_data(ttl=86400)
def search_pubmed(query: str, max_results: int = 10, sort_by: str = "relevance"):
    """
    دالة البحث الأساسية مع دعم التخزين المؤقت وإمكانية اختيار نوع الترتيب.
    sort_by: 'relevance' أو 'pub_date'
    """
    optimized_query = optimize_query(query)
    if not optimized_query:
        return []

    try:
        handle = Entrez.esearch(
            db="pubmed",
            term=optimized_query,
            retmax=max_results,
            sort=sort_by
        )
        results = Entrez.read(handle)
        handle.close()

        ids = results.get("IdList", [])
        if not ids:
            return []

        return get_details(ids)

    except Exception as e:
        print(f"PubMed Search Error: {e}")
        return []


# =====================================
# Paper Details Extraction
# =====================================

def get_details(ids: list) -> list:
    papers = []

    try:
        handle = Entrez.efetch(
            db="pubmed",
            id=",".join(ids),
            rettype="medline",
            retmode="xml"
        )
        records = Entrez.read(handle)
        handle.close()
    except Exception as e:
        print(f"PubMed Fetch Error: {e}")
        return []

    for article in records.get("PubmedArticle", []):

        if is_animal_study(article):
            continue

        citation = article["MedlineCitation"]
        article_data = citation["Article"]

        # 1. Title
        title = str(article_data.get("ArticleTitle", ""))

        # 2. Abstract
        abstract = ""
        try:
            if "Abstract" in article_data and "AbstractText" in article_data["Abstract"]:
                abstract = " ".join([str(x) for x in article_data["Abstract"]["AbstractText"]])
        except Exception:
            pass

        # 3. PMID
        pmid = str(citation.get("PMID", ""))

        # 4. Publication Type
        publication_type = ""
        try:
            publication_type = ", ".join([str(x) for x in article_data.get("PublicationTypeList", [])])
        except Exception:
            pass

        if is_low_evidence_study(publication_type):
            continue

        # 5. Year Parsing (Robust Extraction)
        year = ""
        try:
            pubdate = article_data["Journal"]["JournalIssue"]["PubDate"]
            if "Year" in pubdate:
                year = str(pubdate["Year"])
            elif "MedlineDate" in pubdate:
                match = re.search(r"\d{4}", str(pubdate["MedlineDate"]))
                if match:
                    year = match.group(0)
        except Exception:
            pass

        # 6. Authors Extraction
        authors = []
        try:
            for author in article_data.get("AuthorList", []):
                lastname = author.get("LastName", "")
                initials = author.get("Initials", "")
                if lastname:
                    authors.append(f"{lastname} {initials}".strip())
        except Exception:
            pass

        # 7. DOI Extraction
        doi = ""
        try:
            for item in article.get("PubmedData", {}).get("ArticleIdList", []):
                if item.attributes.get("IdType") == "doi":
                    doi = str(item)
                    break
        except Exception:
            pass

        # 8. Journal Title
        journal_title = ""
        try:
            journal_title = str(article_data["Journal"].get("Title", ""))
        except Exception:
            pass

        evidence_level = classify_evidence_level(publication_type)

        papers.append({
            "pmid": pmid,
            "title": title,
            "authors": authors,
            "journal": journal_title,
            "year": year,
            "doi": doi,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "publication_type": publication_type,
            "evidence_level": evidence_level,
            "abstract": abstract,
            "source": "PubMed",
            "citation_count": None  # غير متوفر بشكل مباشر في Entrez API
        })

    return papers
