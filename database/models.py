from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True)

    title = Column(String)
    field = Column(String)
    research_type = Column(String)

    notes = Column(Text)

    papers = relationship(
        "ResearchPaper",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    questions = relationship(
        "ResearchQuestion",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id = Column(Integer, primary_key=True)

    project_id = Column(
        Integer,
        ForeignKey("research_projects.id")
    )

    title = Column(String)

    abstract = Column(Text)

    pmid = Column(
        String,
        unique=True
    )

    doi = Column(
        String,
        unique=True
    )

    authors = Column(Text)

    journal = Column(String)

    publication_year = Column(String)

    publication_date = Column(String)

    publication_type = Column(Text)

    mesh_terms = Column(Text)

    language = Column(String)

    country = Column(String)

    url = Column(String)

    status = Column(
        String,
        default="Saved"
    )

    notes = Column(Text)

    project = relationship(
        "ResearchProject",
        back_populates="papers"
    )


class ResearchQuestion(Base):
    __tablename__ = "research_questions"

    id = Column(Integer, primary_key=True)

    project_id = Column(
        Integer,
        ForeignKey("research_projects.id")
    )

    population = Column(String)

    intervention = Column(String)

    comparison = Column(String)

    outcome = Column(String)

    question = Column(Text)

    keywords = Column(Text)

    project = relationship(
        "ResearchProject",
        back_populates="questions"
    )
class EvidenceExtraction(Base):
    __tablename__ = "evidence_extractions"

    id = Column(Integer, primary_key=True)

    article_id = Column(String)

    doi = Column(String)

    pmid = Column(String)

    population = Column(Text)

    intervention = Column(Text)

    comparator = Column(Text)

    outcome = Column(Text)

    study_design = Column(String)

    risk_of_bias = Column(String)

    notes = Column(Text)

    updated_at = Column(String)
