from database.db import SessionLocal
from database.models import ResearchPaper


def save_paper(
    project_id,
    paper
):

    db = SessionLocal()

    doi = paper.get("doi", "")

    # منع التكرار إذا كان DOI موجوداً
    if doi:

        existing = db.query(
            ResearchPaper
        ).filter(
            ResearchPaper.doi == doi
        ).first()

        if existing:

            db.close()

            return {
                "saved": False,
                "message": "Paper already exists"
            }

    paper_record = ResearchPaper(
        project_id=project_id,
        title=paper["title"],
        abstract=paper["abstract"],
        doi=doi,
        pubmed_url=paper.get("url", ""),
        authors=paper.get("authors", ""),
        journal=paper.get("journal", ""),
        publication_year=paper.get("year", "")
    )

    db.add(paper_record)

    db.commit()

    db.close()

    return {
        "saved": True,
        "message": "Paper saved"
    }


def get_papers(project_id):

    db = SessionLocal()

    papers = db.query(
        ResearchPaper
    ).filter(
        ResearchPaper.project_id == project_id
    ).order_by(
        ResearchPaper.publication_year.desc().nullslast()
    ).all()

    db.close()

    return papers
