import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

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


Base.metadata.create_all(bind=engine)


st.set_page_config(
    page_title="Med Research Copilot",
    page_icon="🧬",
    layout="wide"
)


st.title("🧬 Med Research Copilot")

st.subheader(
    "AI Assistant for Medical Research"
)

# --- تم تعطيل رافع الملفات العام المؤقت لعدم الحاجة إليه هنا ---
# uploaded_file = st.file_uploader(
#     "Upload Dataset",
#     type=["csv", "xlsx", "xls"]
# )
# if uploaded_file:
#     df, report = analyze_dataset(uploaded_file)
#     ...


menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "New Research Project",
        "Research Idea Generator",
        "Research Question Builder",
        "Protocol Builder",
        "📋 Statistical Planning",
        "Data Analysis",
        "📊 Statistical Analysis",
        "Literature Search",
        "Research Library",
        "Paper Analyzer"
    ]
)


if menu == "Dashboard":

    st.write(
        """
        Welcome to Med Research Copilot.

        Your assistant from research idea
        to scientific publication.
        """
    )


elif menu == "New Research Project":

    st.header("Create Research Project")

    title = st.text_input(
        "Research Title"
    )

    field = st.text_input(
        "Medical Field"
    )

    research_type = st.selectbox(
        "Research Type",
        [
            "Clinical Trial",
            "Systematic Review",
            "Cohort Study",
            "Case Report"
        ]
    )

    if st.button("Save Project"):

        st.success(
            "Project created successfully"
        )


elif menu == "Research Idea Generator":

    st.header(
        "💡 AI Research Idea Generator"
    )

    field = st.text_input(
        "Enter medical field"
    )

    if st.button("Generate Ideas"):

        if field:

            with st.spinner(
                "Generating research ideas..."
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

        else:

            st.warning(
                "Please enter a medical field first."
            )


elif menu == "Research Question Builder":

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


elif menu == "Protocol Builder":

    st.header(
        "📋 Research Protocol Builder"
    )

    idea = st.text_area(
        "Enter research idea"
    )

    if st.button("Generate Protocol"):

        with st.spinner(
            "Building protocol..."
        ):

            protocol = generate_protocol(
                idea
            )

        st.markdown(protocol)


elif menu == "📋 Statistical Planning":

    from research_analytics.smart_selector import suggest_test

    st.header("📊 AI Statistical Advisor")

    outcome_type = st.selectbox(
        "Outcome Type",
        [
            "continuous",
            "categorical"
        ]
    )

    groups = st.number_input(
        "Number of Groups",
        min_value=2,
        value=2
    )

    objective = st.selectbox(
        "Objective",
        [
            "comparison",
            "correlation"
        ]
    )

    paired = st.checkbox(
        "Paired Data"
    )

    normal_distribution = st.checkbox(
        "Normally Distributed",
        value=True
    )

    if st.button(
        "Recommend Test"
    ):

        result = suggest_test(
            outcome_type=outcome_type,
            groups=groups,
            objective=objective,
            paired=paired,
            normal_distribution=normal_distribution
        )

        st.success(result["test"])

        st.write(result["reason"])

        if "alternative" in result:

            st.info(
                f"Alternative: {result['alternative']}"
            )


elif menu == "Data Analysis":

    st.header(
        "📊 Medical Data Profiler"
    )

    # --- تم تعطيل رافع الملفات هنا مؤقتاً لتجنب أي تداخل مع صفحات التحليل الأخرى ---
    # uploaded_file = st.file_uploader(
    #     "Upload Dataset",
    #     type=["csv", "xlsx", "xls"],
    #     key="data_analysis_uploader"
    # )
    # if uploaded_file:
    #     df, report = analyze_dataset(uploaded_file)
    #     st.success("Dataset loaded successfully")
    #     ...
    
    st.info("Data analysis components are being managed via Analytics module.")


elif menu == "📊 Statistical Analysis":

    from pages.analytics_page import render

    render()


elif menu == "Literature Search":

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
