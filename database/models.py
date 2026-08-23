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

    # علاقة تمكنك من الوصول لكل الأوراق البحثية التابعة للمشروع (papers)
    papers = relationship("ResearchPaper", back_populates="project", cascade="all, delete-orphan")


class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"))
    title = Column(String)
    abstract = Column(Text)
    status = Column(String, default="Saved")
    notes = Column(Text)

    # علاقة تمكنك من الوصول للمشروع التابع له الورقة البحثية (project)
    project = relationship("ResearchProject", back_populates="papers")
