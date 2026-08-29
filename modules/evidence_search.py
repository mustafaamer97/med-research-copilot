from modules.pubmed import search_pubmed

PRIORITY_FILTERS = [
    "systematic review",
    "meta-analysis",
    "randomized controlled trial",
    "clinical trial",
    "cohort study",
    "observational study"
]

EXCLUDED_TYPES = ["editorial", "letter", "comment", "case reports"]


def get_recent_evidence(topic, current_year=2026, recent_cutoff_years=5):
    all_papers = []

    # 1. بحث عام أولاً لتغطية المواضيع الضيقة (مثل البحث الجغرافي)
    try:
        general_papers = search_pubmed(topic, max_results=20)
        all_papers.extend(general_papers)
    except Exception as e:
        print(f"General evidence search error: {e}")

    # 2. البحث التخصصي باستخدام الفلاتر مع تحديد حد أقصى لكل نوع (max_per_type = 5)
    for study_type in PRIORITY_FILTERS:
        query = f"{topic} AND {study_type}"
        try:
            papers = search_pubmed(query, max_results=5)
            all_papers.extend(papers)
        except Exception as e:
            print(f"Evidence search error ({study_type}): {e}")

    # 3. إزالة التكرار (PMID ثم Title) واستبعاد المقالات منخفضة الجودة
    unique_papers = {}
    for paper in all_papers:
        pub_type = str(paper.get("publication_type", "")).lower()
        if any(excluded in pub_type for excluded in EXCLUDED_TYPES):
            continue

        # ضمان وجود الحقول الأساسية حتى لا ينكسر Gap Analysis
        normalized_paper = {
            "pmid": paper.get("pmid", ""),
            "title": paper.get("title", ""),
            "abstract": paper.get("abstract", ""),
            "year": int(paper.get("year", 0)) if str(paper.get("year", "")).isdigit() else 0,
            "journal": paper.get("journal", "Unknown"),
            "publication_type": paper.get("publication_type", "Journal Article"),
            "evidence_level": paper.get("evidence_level", "Unknown")
        }

        key = normalized_paper["pmid"] if normalized_paper["pmid"] else normalized_paper["title"].strip().lower()
        if key and key not in unique_papers:
            unique_papers[key] = normalized_paper

    papers = list(unique_papers.values())

    # 4. الترتيب المزدوج: level of evidence أولاً، ثم الحداثة (السنة الأحدث أولاً)
    ranking = {
        "Level 1": 1,
        "Level 2": 2,
        "Level 3": 3,
        "Level 4": 4,
        "Level 5": 5,
        "Unknown": 99
    }

    papers.sort(
        key=lambda p: (
            ranking.get(p.get("evidence_level", "Unknown"), 99),
            -p.get("year", 0)
        )
    )

    selected_papers = papers[:20]

    # 5. حساب نسبة الأدلة الحديثة (Recent Evidence %)
    cutoff_year = current_year - recent_cutoff_years
    recent_count = sum(1 for p in selected_papers if p.get("year", 0) >= cutoff_year)
    total_count = len(selected_papers)
    recent_evidence_pct = (recent_count / total_count * 100) if total_count > 0 else 0.0

    return {
        "papers": selected_papers,
        "metrics": {
            "total_papers": total_count,
            "recent_papers_count": recent_count,
            "recent_evidence_pct": round(recent_evidence_pct, 1)
        }
    }
