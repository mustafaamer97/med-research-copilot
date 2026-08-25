import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --- استيراد خطوات سير العمل (Workflow Steps 1–5) ---
from workflow.step1_context import render as step1_render
from workflow.step2_idea import render as step2_render
from workflow.step3_question import render as step3_render
from workflow.step4_literature import render as step4_render
from workflow.step5_protocol import render as step5_render

# --- استيراد خطوات سير العمل (Workflow Steps 6–10) ---
from components.step6_sample_size import render_step6
from components.step7_irb import render_step7
from components.step8_data_collection import render_step8
from components.step9_statistics import render_step9
from components.step10_manuscript import render_step10

# --- الاستيرادات الأخرى والأدوات ---
from database.db import engine
from database.models import Base
from modules.library import get_papers, search_papers
from utils.pdf_tools import extract_text
from modules.paper_analyzer import analyze_paper
from modules.paper_reviewer import review_paper

# إنشاء الجداول في قاعدة البيانات إن لم تكن موجودة
Base.metadata.create_all(bind=engine)

# تهيئة سياق البحث في session_state في حال لم يكن معرفاً من قبل
if "research_context" not in st.session_state:
    st.session_state["research_context"] = {}

# =========================
# Workflow State
# =========================

if "selected_research_idea" not in st.session_state:
    st.session_state["selected_research_idea"] = {}

if "research_question" not in st.session_state:
    st.session_state["research_question"] = {}

if "question_completed" not in st.session_state:
    st.session_state["question_completed"] = False

if "literature_search" not in st.session_state:
    st.session_state["literature_search"] = {}

if "research_protocol" not in st.session_state:
    st.session_state["research_protocol"] = {}

if "sample_size_plan" not in st.session_state:
    st.session_state["sample_size_plan"] = {}

if "irb_package" not in st.session_state:
    st.session_state["irb_package"] = {}

if "data_collection_plan" not in st.session_state:
    st.session_state["data_collection_plan"] = {}

if "statistical_plan" not in st.session_state:
    st.session_state["statistical_plan"] = {}

if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = {}

if "manuscript_package" not in st.session_state:
    st.session_state["manuscript_package"] = {}

# =========================
# Workflow Completion Flags
# =========================

WORKFLOW_STEPS = {
    "context_completed": False,
    "idea_completed": False,
    "question_completed": False,
    "literature_completed": False,
    "protocol_completed": False,
    "sample_size_completed": False,
    "irb_completed": False,
    "data_collection_completed": False,
    "analysis_completed": False,
    "manuscript_completed": False,
}

for key, value in WORKFLOW_STEPS.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.set_page_config(
    page_title="Med Research Copilot",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Med Research Copilot")

st.subheader(
    "AI Assistant for Medical Research"
)

# --- القائمة الجانبية التنقلية ---
st.sidebar.title("🧬 Research Workflow")

menu = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",

        "──────── PHASE 1 ────────",
        "Step 1: Context & Scope Builder",
        "Step 2: Idea Generator & Validation",
        "Step 3: Research Question Builder",

        "──────── PHASE 2 ────────",
        "Step 4: Literature Search & Analyzer",
        "Step 5: Protocol Builder",

        "──────── PHASE 3 ────────",
        "Step 6: Sample Size & Power",
        "Step 7: Ethics & IRB",

        "──────── PHASE 4 ────────",
        "Step 8: Data Collection",

        "──────── PHASE 5 ────────",
        "Step 9: Statistical Analysis",

        "──────── PHASE 6 ────────",
        "Step 10: Manuscript & Journal Finder",

        "──────── TOOLS ────────",
        "Research Library",
        "Paper Analyzer"
    ]
)

# --- التنقل وتنفيذ الدعم البرمجي لكل خطوة ---

if menu == "🏠 Dashboard":

    st.write(
        """
        Welcome to Med Research Copilot.

        Your assistant from research idea
        to scientific publication.
        """
    )

elif menu == "Step 1: Context & Scope Builder":
    step1_render()

elif menu == "Step 2: Idea Generator & Validation":
    step2_render()

elif menu == "Step 3: Research Question Builder":
    step3_render()

elif menu == "Step 4: Literature Search & Analyzer":
    step4_render()

elif menu == "Step 5: Protocol Builder":
    step5_render()

elif menu == "Step 6: Sample Size & Power":
    render_step6()

elif menu == "Step 7: Ethics & IRB":
    render_step7()

elif menu == "Step 8: Data Collection":
    render_step8()

elif menu == "Step 9: Statistical Analysis":
    render_step9()

elif menu == "Step 10: Manuscript & Journal Finder":
    render_step10()

elif menu == "Research Library":

    st.header(
        "📚 Research Library"
    )

    project_id = st.number_input(
        "Project ID",
        min_value=1
    )

    search_term = st.text_input(
        "Search Title, DOI or Author"
    )

    if st.button("Load Papers"):

        if search_term:

            papers = search_papers(
                project_id,
                search_term
            )

        else:

            papers = get_papers(
                project_id
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Papers",
                len(papers)
            )

        with col2:

            doi_count = len(
                [
                    p for p in papers
                    if getattr(p, "doi", None)
                ]
            )

            st.metric(
                "Papers with DOI",
                doi_count
            )

        with col3:

            journal_count = len(
                set(
                    [
                        p.journal
                        for p in papers
                        if getattr(
                            p,
                            "journal",
                            None
                        )
                    ]
                )
            )

            st.metric(
                "Journals",
                journal_count
            )

        years = sorted(
            list(
                set(
                    [
                        p.publication_year
                        for p in papers
                        if getattr(
                            p,
                            "publication_year",
                            None
                        )
                    ]
                )
            ),
            reverse=True
        )

        selected_year = st.selectbox(
            "Filter by Year",
            ["All"] + years
        )

        if selected_year != "All":

            papers = [
                p
                for p in papers
                if p.publication_year == selected_year
            ]

        if papers:

            for paper in papers:

                st.subheader(
                    paper.title
                )

                if paper.authors:

                    st.write(
                        f"Authors: {paper.authors}"
                    )

                if paper.journal:

                    st.write(
                        f"Journal: {paper.journal}"
                    )

                if paper.publication_year:

                    st.write(
                        f"Year: {paper.publication_year}"
                    )

                if paper.doi:

                    st.write(
                        f"DOI: {paper.doi}"
                    )

                if paper.pubmed_url:

                    st.markdown(
                        f"[Open in PubMed]({paper.pubmed_url})"
                    )

                st.write(
                    paper.abstract
                )

                st.divider()

        else:

            st.info(
                "No saved papers for this project ID."
            )

elif menu == "Paper Analyzer":

    st.header(
        "📄 Scientific Paper Analyzer"
    )

    file = st.file_uploader(
        "Upload Research PDF",
        type=["pdf"]
    )

    if file:

        with st.spinner(
            "Analyzing paper..."
        ):

            text = extract_text(file)

            analysis = analyze_paper(text)

        st.subheader(
            "Research Summary"
        )

        for key, value in analysis.items():

            st.markdown(
                f"### {key}"
            )

            if isinstance(value, dict):

                st.json(value)

            else:

                st.write(value)

        st.divider()

        if st.button("AI Review"):

            with st.spinner(
                "AI is reviewing the paper..."
            ):

                review = review_paper(text)

            st.subheader(
                "🧠 AI Research Review"
            )

            st.write(review)
