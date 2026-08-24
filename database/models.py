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

    # العلاقات مع الجداول الأخرى
    papers = relationship("ResearchPaper", back_populates="project", cascade="all, delete-orphan")
    questions = relationship("ResearchQuestion", back_populates="project", cascade="all, delete-orphan")


class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id = Column(Integer, primary_key=True)

    project_id = Column(
        Integer,
        ForeignKey("research_projects.id")
    )

    pmid = Column(String)

    title = Column(Text)

    authors = Column(Text)

    journal = Column(String)

    publication_year = Column(String)

    doi = Column(String)

    pubmed_url = Column(Text)

    abstract = Column(Text)

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
    project_id = Column(Integer, ForeignKey("research_projects.id"))

    population = Column(String)
    intervention = Column(String)
    comparison = Column(String)
    outcome = Column(String)
    question = Column(Text)
    keywords = Column(Text)

    # العلاقة العكسية مع المشروع
    project = relationship("ResearchProject", back_populates="questions")
