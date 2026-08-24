from database.db import SessionLocal
from database.models import ResearchPaper


def save_paper(
    project_id,
    paper
):

    db = SessionLocal()

    doi = paper.get("doi", "")
    pmid = paper.get("pmid", "")

    # منع التكرار بواسطة DOI
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
                "message": "Paper already exists (DOI)"
            }

    # منع التكرار بواسطة PMID
    elif pmid:

        existing = db.query(
            ResearchPaper
        ).filter(
            ResearchPaper.pmid == pmid
        ).first()

        if existing:

            db.close()

            return {
                "saved": False,
                "message": "Paper already exists (PMID)"
            }

    paper_record = ResearchPaper(
        project_id=project_id,
        title=paper.get("title", ""),
        abstract=paper.get("abstract", ""),
        pmid=pmid,
        doi=doi,
        authors=paper.get("authors", ""),
        journal=paper.get("journal", ""),
        publication_year=paper.get("year", ""),
        url=paper.get("url", "")
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


def search_papers(
    project_id,
    search_term
):

    db = SessionLocal()

    papers = db.query(
        ResearchPaper
    ).filter(
        ResearchPaper.project_id == project_id,
        (
            ResearchPaper.title.contains(search_term)
        )
        |
        (
            ResearchPaper.doi.contains(search_term)
        )
        |
        (
            ResearchPaper.pmid.contains(search_term)
        )
        |
        (
            ResearchPaper.authors.contains(search_term)
        )
        |
        (
            ResearchPaper.journal.contains(search_term)
        )
    ).all()

    db.close()

    return papers
