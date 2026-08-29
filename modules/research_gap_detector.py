from collections import Counter
from datetime import datetime
import re


def detect_research_gaps(papers, target_country="Yemen"):
    keyword_counter = Counter()
    publication_types = Counter()
    journals = Counter()
    study_designs = Counter()
    countries = Counter()

    total_papers = len(papers)
    if total_papers == 0:
        return {
            "total_papers": 0,
            "gap_score": 0,
            "research_gaps": ["No papers provided for analysis."],
            "top_keywords": [],
            "study_types": [],
            "top_journals": [],
            "top_countries": [],
        }

    current_year = datetime.now().year
    five_years_ago = current_year - 5

    recent_studies_count = 0

    for paper in papers:
        # 1. Keywords extraction
        title = paper.get("title", "").lower()
        words = re.findall(r"\b[a-zA-Z]{4,}\b", title)
        keyword_counter.update(words)

        # 2. Publication types & Journals
        pub_type = paper.get("publication_type", "")
        if pub_type:
            publication_types.update([pub_type])

        journal = paper.get("journal", "")
        if journal:
            journals.update([journal])

        # 3. Study Design
        design = paper.get("study_design") or paper.get("design", "")
        if design:
            study_designs.update([str(design)])

        # 4. Country / Affiliation
        country = (
            paper.get("country")
            or paper.get("affiliation_country")
            or paper.get("location", "")
        )
        if country:
            countries.update([str(country).strip()])

        # 5. Publication Year check
        year = paper.get("year")
        try:
            if year and int(year) >= five_years_ago:
                recent_studies_count += 1
        except (ValueError, TypeError):
            pass

    gaps = []

    # --- Gap Analysis Checks ---

    # 1. Level 1 Evidence
    level1_count = len(
        [p for p in papers if p.get("evidence_level") == "Level 1"]
    )
    if level1_count == 0:
        gaps.append("No systematic reviews or meta-analyses identified.")

    # 2. Clinical Trials
    trial_count = len(
        [
            p
            for p in papers
            if "trial" in str(p.get("publication_type", "")).lower()
        ]
    )
    if trial_count < 3:
        gaps.append("Limited randomized or clinical trial evidence.")

    # 3. Sample / Evidence Base Size
    if total_papers < 10:
        gaps.append("Small overall evidence base available.")

    # 4. Journal Concentration
    if len(journals) < 3:
        gaps.append("Evidence concentrated in very few journals.")

    # 5. Recent Evidence Gap (NEW)
    recent_percentage = (recent_studies_count / total_papers) * 100
    if recent_percentage < 30:
        gaps.append(
            f"Limited recent evidence: only {recent_percentage:.1f}% published in the last 5 years."
        )

    # 6. Study Design Diversity Gap (NEW)
    if len(study_designs) < 3:
        gaps.append(
            "Limited diversity of study designs (mostly single methodology)."
        )

    # 7. Local Evidence Gap (NEW)
    country_list_normalized = [c.lower() for c in countries.keys()]
    if target_country.lower() not in country_list_normalized:
        gaps.append(
            f"No local studies identified specifically from {target_country}."
        )

    # --- Gap Score Calculation (NEW) ---
    # Deduct 12 points per gap detected
    gap_score = max(0, 100 - (len(gaps) * 12))

    return {
        "total_papers": total_papers,
        "gap_score": gap_score,
        "recent_studies_percentage": round(recent_percentage, 1),
        "top_keywords": keyword_counter.most_common(20),
        "study_types": publication_types.most_common(10),
        "study_designs": study_designs.most_common(10),
        "top_journals": journals.most_common(10),
        "top_countries": countries.most_common(10),
        "research_gaps": gaps,
    }
