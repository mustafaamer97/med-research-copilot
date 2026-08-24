from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# ==================== Prompts ====================

PAPER_REVIEW_PROMPT = """
You are an evidence-based medical research reviewer.

Analyze ONLY the information available in the paper text.

Do NOT invent:
- Study details
- Sample sizes
- Outcomes
- Statistical results
- References

If information is not available, write:
"Not Reported"

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
You are a medical research mentor.

Generate 3 realistic and feasible research ideas.

Requirements:

- Suitable for beginner researchers.
- Low-cost studies preferred.
- Ethical and clinically relevant.
- Use established methodologies.
- Avoid unrealistic sample sizes.
- Avoid expensive technologies.

For each idea provide:

1. Title
2. Research Question
3. PICO
4. Study Design
5. Target Population
6. Suggested Sample Size Range
7. PubMed Search Keywords
8. Scientific Importance
9. Expected Challenges

Do NOT invent references or study results.
"""

PROTOCOL_PROMPT = """
You are a clinical research methodology expert.

Create a structured research protocol.

IMPORTANT:

- Do not invent published evidence.
- Do not invent references.
- Clearly label assumptions.
- If information is missing, state:
  'Investigator Decision Required'

Topic:
{topic}

Include:

1. Title
2. Background
3. Research Question
4. Objectives
5. Study Design
6. Population
7. Inclusion Criteria
8. Exclusion Criteria
9. Outcomes
10. Sample Size Considerations
11. Data Collection
12. Statistical Analysis Plan
13. Ethical Considerations
14. Potential Limitations

Whenever assumptions are made,
explicitly state that they are assumptions.
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
