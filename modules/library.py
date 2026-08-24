from database.db import SessionLocal
from database.models import ResearchPaper


def save_paper(
    project_id,
    paper
):

    db = SessionLocal()

    paper_record = ResearchPaper(
        project_id=project_id,
        title=paper["title"],
        abstract=paper["abstract"],
        doi=paper.get("doi", ""),
        pubmed_url=paper.get("url", "")
    )

    db.add(paper_record)

    db.commit()

    db.close()


def get_papers(project_id):

    db = SessionLocal()

    papers = db.query(
        ResearchPaper
    ).filter(
        ResearchPaper.project_id == project_id
    ).all()

    db.close()

    return papers
