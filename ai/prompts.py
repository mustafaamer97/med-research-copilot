from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# ==================== Prompts ====================

PAPER_REVIEW_PROMPT = """
You are a medical research expert.

Analyze this scientific paper.

Provide:
1. Study design
2. Research question
3. Population
4. Intervention
5. Outcomes
6. Main findings
7. Strengths
8. Limitations
9. Risk of bias
10. Evidence quality

Paper text:
{text}
"""

RESEARCH_IDEA_PROMPT = """
You are an expert medical researcher.

Generate research ideas for:

Medical field:
{field}

Provide:
1. Research title
2. Research question
3. PICO framework
4. Suggested study design
5. PubMed keywords
6. Scientific importance

Make ideas suitable for beginner researchers.
"""

# ==================== Database Models ====================

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
    project_id = Column(Integer, ForeignKey("research_projects.id"))
    title = Column(String)
    abstract = Column(Text)
    status = Column(String, default="Saved")
    notes = Column(Text)

    # العلاقة العكسية مع المشروع
    project = relationship("ResearchProject", back_populates="papers")


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
