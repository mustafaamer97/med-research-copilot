from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ResearchProject(Base):

    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    field = Column(String)

    research_type = Column(String)

    notes = Column(Text)
