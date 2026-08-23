from database.db import SessionLocal
from database.models import ResearchPaper



def save_paper(
    project_id,
    title,
    abstract
):

    db = SessionLocal()

    paper = ResearchPaper(
        project_id=project_id,
        title=title,
        abstract=abstract
    )

    db.add(paper)

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
