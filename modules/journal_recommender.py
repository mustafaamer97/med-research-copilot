from collections import Counter

# قاعدة بيانات المجلات المرجعية للـ Q1/Q2 والتخصصات وانواع الدراسات
TOP_MEDICAL_JOURNALS = {
    "The Lancet": {
        "fields": ["General Medicine", "Internal Medicine", "Public Health"],
        "tier": "Q1",
        "preferred_designs": ["RCT", "Systematic Review", "Meta-Analysis", "Cohort Study"]
    },
    "New England Journal of Medicine": {
        "fields": ["General Medicine", "Internal Medicine"],
        "tier": "Q1",
        "preferred_designs": ["RCT", "Clinical Trial", "Cohort Study"]
    },
    "JAMA": {
        "fields": ["General Medicine", "Internal Medicine", "Public Health"],
        "tier": "Q1",
        "preferred_designs": ["RCT", "Systematic Review", "Cohort Study"]
    },
    "BMJ": {
        "fields": ["General Medicine", "Public Health"],
        "tier": "Q1",
        "preferred_designs": ["RCT", "Systematic Review", "Observational Study"]
    },
    "Journal of Clinical Oncology": {
        "fields": ["Oncology", "Cancer Research"],
        "tier": "Q1",
        "preferred_designs": ["RCT", "Clinical Trial", "Cohort Study"]
    },
    "Cancer Medicine": {
        "fields": ["Oncology", "Cancer Research"],
        "tier": "Q2",
        "preferred_designs": ["Cohort Study", "Cross-Sectional", "Case-Control"]
    },
    "BMC Cancer": {
        "fields": ["Oncology", "Cancer Research"],
        "tier": "Q2",
        "preferred_designs": ["Cohort Study", "Cross-Sectional", "Case-Control", "RCT"]
    },
    "PLOS ONE": {
        "fields": ["Multidisciplinary", "General Medicine"],
        "tier": "Q2",
        "preferred_designs": ["Cross-Sectional", "Cohort Study", "Case-Control", "Survey"]
    }
}


def recommend_journals(
    literature: list,
    medical_field: str = "",
    study_design: str = ""
) -> list:
    """
    Recommends target journals based on literature presence, medical field,
    and study design match, returning a scored and sorted list of recommendations.
    """
    # 1. استخراج وعدّ المجلات من الأدبيات الممررة
    raw_journals = [
        paper.get("journal", "").strip() 
        for paper in literature 
        if paper.get("journal")
    ]
    literature_counts = Counter(raw_journals)

    # 2. حصر جميع المجلات (الموجودة في الأدبيات + المجلات المرجعية)
    all_candidate_journals = set(literature_counts.keys()).union(TOP_MEDICAL_JOURNALS.keys())

    field_clean = medical_field.strip().lower()
    design_clean = study_design.strip().lower()

    scored_recommendations = []

    for journal in all_candidate_journals:
        if not journal:
            continue

        paper_count = literature_counts.get(journal, 0)
        journal_info = TOP_MEDICAL_JOURNALS.get(journal, {})

        tier = journal_info.get("tier", "Unranked / Local")
        supported_fields = [f.lower() for f in journal_info.get("fields", [])]
        preferred_designs = [d.lower() for d in journal_info.get("preferred_designs", [])]

        # فحص المطابقة
        field_match = any(field_clean in f or f in field_clean for f in supported_fields) if field_clean else False
        design_match = any(design_clean in d or d in design_clean for d in preferred_designs) if design_clean else False

        # نظام نقاط التوصية (Score Calculation)
        score = 0.0

        # أوزان ظهور الأدبيات
        score += paper_count * 2.0

        # أوزان التخصص ونوع الدراسة
        if field_match:
            score += 3.0
        if design_match:
            score += 2.5

        # وزن التصنيف (Tier)
        if tier == "Q1":
            score += 2.0
        elif tier == "Q2":
            score += 1.0

        # تضمين المجلة إذا كانت مكررة في Literature أو تطابق التخصص/النوع
        if paper_count > 0 or field_match or design_match:
            scored_recommendations.append({
                "journal": journal,
                "score": round(score, 2),
                "supporting_papers": paper_count,
                "tier": tier,
                "field_match": field_match,
                "study_design_match": design_match
            })

    # 3. ترتيب المجلات بناءً على الـ Score التراكمي
    scored_recommendations.sort(key=lambda x: x["score"], reverse=True)

    return scored_recommendations[:10]
