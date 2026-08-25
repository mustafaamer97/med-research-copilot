import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --- الاستيرادات ---
from components.step1_field import render_step1
from research_analytics.data_checker import analyze_dataset
from database.db import engine
from database.models import Base
from modules.pubmed import search_pubmed
from modules.library import (
    save_paper,
    get_papers,
    search_papers
)
from utils.pdf_tools import extract_text
from modules.paper_analyzer import analyze_paper
from modules.paper_reviewer import review_paper
from modules.idea_generator import generate_research_ideas
from modules.protocol_builder import generate_protocol


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


# --- معالجة الشروط بناءً على القائمة المحدثة ---

if menu == "🏠 Dashboard":

    st.write(
        """
        Welcome to Med Research Copilot.

        Your assistant from research idea
        to scientific publication.
        """
    )


elif menu == "Step 1: Context & Scope Builder":

    render_step1()


elif menu == "Step 2: Idea Generator & Validation":

    st.header(
        "💡 Research Idea Workspace"
    )

    mode = st.radio(
        "Choose Workflow",
        [
            "Generate New Research Idea",
            "I Already Have a Research Idea"
        ]
    )

    # ==================================
    # PATH A
    # Generate Idea
    # ==================================

    if mode == "Generate New Research Idea":

        default_field = (
            st.session_state["research_context"]
            .get("field", "")
        )

        field = st.text_input(
            "Medical Field",
            value=default_field
        )

        if st.button(
            "Generate Ideas"
        ):

            if field:

                with st.spinner(
                    "Generating ideas..."
                ):

                    ideas = generate_research_ideas(
                        field
                    )

                st.subheader(
                    "Suggested Research Ideas"
                )

                st.write(
                    ideas
                )

                st.session_state[
                    "generated_ideas"
                ] = ideas

            else:

                st.warning(
                    "Please select a field first."
                )

    # ==================================
    # PATH B
    # Existing Idea
    # ==================================

    else:

        st.info(
            "Enter your existing research idea."
        )

        idea_title = st.text_input(
            "Research Idea Title"
        )

        idea_description = st.text_area(
            "Research Idea Description"
        )

        if st.button(
            "Save Research Idea"
        ):

            st.session_state[
                "selected_research_idea"
            ] = {
                "title": idea_title,
                "description": idea_description
            }

            st.success(
                "Research idea saved successfully."
            )

            st.json(
                st.session_state[
                    "selected_research_idea"
                ]
            )


elif menu == "Step 3: Research Question Builder":

    if not st.session_state["idea_completed"]:

        st.warning(
            "Please complete Step 2 first."
        )

        st.stop()

    idea_data = st.session_state.get(
        "selected_research_idea",
        {}
    )

    if idea_data:

        st.info(
            f"""
Selected Idea:

{idea_data.get('title','')}
"""
        )

    st.header(
        "🧬 PICO Research Question Builder"
    )

    population = st.text_input(
        "Population (P)"
    )

    intervention = st.text_input(
        "Intervention (I)"
    )

    comparison = st.text_input(
        "Comparison (C)"
    )

    outcome = st.text_input(
        "Outcome (O)"
    )

    if st.button("Generate Research Question"):

        from modules.pico_builder import build_pico

        result = build_pico(
            population,
            intervention,
            comparison,
            outcome
        )

        st.subheader(
            "Research Question"
        )

        st.write(
            result["question"]
        )

        st.subheader(
            "PubMed Search Keywords"
        )

        st.code(
            result["keywords"]
        )


elif menu == "Step 4: Literature Search & Analyzer":

    if not st.session_state["question_completed"]:

        st.warning(
            "Please complete Step 3 first."
        )

        st.stop()

    st.header(
        "🔎 PubMed Literature Search"
    )

    query = st.text_input(
        "Enter medical topic"
    )

    number = st.slider(
        "Number of papers",
        1,
        20,
        5
    )

    if st.button("Search PubMed"):

        with st.spinner("Searching medical literature..."):

            papers = search_pubmed(
                query,
                number
            )

        if papers:

            for idx, paper in enumerate(papers):

                st.subheader(
                    paper["title"]
                )

                if paper.get("doi"):
                    st.write("DOI:", paper["doi"])

                if paper.get("url"):
                    st.markdown(
                        f"[Open in PubMed]({paper['url']})"
                    )

                st.write(
                    paper["abstract"]
                )

                if st.button(f"Save Paper", key=f"save_{idx}"):

                    result = save_paper(
                        project_id=1,
                        paper=paper
                    )

                    if result["saved"]:

                        st.success(
                            result["message"]
                        )

                    else:

                        st.warning(
                            result["message"]
                        )

                st.divider()

        else:

            st.warning(
                "No papers found"
            )


elif menu == "Step 5: Protocol Builder":

    st.header(
        "📋 Research Protocol Builder"
    )

    idea = st.text_area(
        "Enter research idea"
    )

    study_type = st.selectbox(
        "Study Type",
        [
            "Clinical Trial",
            "Cohort Study",
            "Case-Control Study",
            "Cross-Sectional Study",
            "Systematic Review",
            "Meta-analysis"
        ]
    )

    if st.button("Generate Protocol"):

        with st.spinner(
            "Building protocol..."
        ):

            protocol = generate_protocol(
                idea,
                study_type
            )

        st.markdown(protocol)


elif menu == "Step 6: Sample Size & Power":

    st.header(
        "Step 6: Sample Size & Power Calculator"
    )

    st.info(
        "This module will be connected during Phase 3."
    )


elif menu == "Step 7: Ethics & IRB":

    st.header(
        "Step 7: IRB & Ethical Approval"
    )

    st.info(
        "This module will be connected during Phase 3."
    )


elif menu == "Step 8: Data Collection":

    st.header(
        "Step 8: Data Collection Sheet Generator"
    )

    st.info(
        "This module will be connected during Phase 4."
    )


elif menu == "Step 9: Statistical Analysis":

    from pages.analytics_page import render

    render()


elif menu == "Step 10: Manuscript & Journal Finder":

    st.header(
        "Step 10: Manuscript Draft & Journal Finder"
    )

    st.info(
        "This module will be connected during Phase 6."
    )


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

        if (
            selected_year != "All"
        ):

            papers = [
                p
                for p in papers
                if p.publication_year
                == selected_year
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
