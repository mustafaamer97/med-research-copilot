import sys
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from statistics.data_checker import analyze_dataset
from database.db import engine
from database.models import Base
from modules.pubmed import search_pubmed
from modules.library import save_paper, get_papers
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


uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file:

    df, report = analyze_dataset(uploaded_file)

    st.success("Dataset loaded successfully")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Information")
    st.write("Rows:", report["rows"])
    st.write("Columns:", report["columns"])
    st.write("Duplicates:", report["duplicates"])

    st.subheader("Numeric Columns")
    st.write(report["numeric_columns"])

    st.subheader("Categorical Columns")
    st.write(report["categorical_columns"])

    st.subheader("Missing Values")
    st.json(report["missing_percentage"])

    st.subheader("Normality Test")
    st.json(report["normality"])

    st.divider()


menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "New Research Project",
        "Research Idea Generator",
        "Research Question Builder",
        "Protocol Builder",
        "statistical advisor",
        "Data Analysis",
        "statistical analysis",
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


elif menu == "statistical advisor":

    from statistics.test_selector import suggest_test

    st.header(
        "📊 Medical statistical Advisor"
    )

    variable_type = st.selectbox(
        "Outcome variable type",
        [
            "continuous",
            "categorical"
        ]
    )

    groups = st.number_input(
        "Number of groups",
        min_value=1,
        value=2
    )

    objective = st.selectbox(
        "Research objective",
        [
            "comparison",
            "correlation"
        ]
    )

    if st.button("Suggest statistical Test"):

        result = suggest_test(
            variable_type,
            groups,
            objective
        )

        st.success(
            result["test"]
        )

        st.write(
            result["reason"]
        )

        st.info(
            "Alternative: "
            + result.get("alternative", "")
        )


elif menu == "Data Analysis":

    st.header(
        "📊 Medical Data Profiler"
    )

    file = st.file_uploader(
        "Upload CSV or Excel file",
        type=[
            "csv",
            "xlsx"
        ],
        key="data_analysis_uploader"
    )

    if file:

        df_da, report_da = analyze_dataset(file)

        st.subheader(
            "Dataset Preview"
        )

        st.dataframe(df_da.head())

        st.subheader(
            "Dataset Information"
        )

        st.write(
            report_da
        )


elif menu == "statistical analysis":

    from statistics.analysis_engine import run_ttest
    from statistics.report_generator import interpret_p_value

    st.header(
        "📊 Automated statistical Analysis"
    )

    file = st.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx"],
        key="stat_analysis_uploader"
    )

    if file:

        import pandas as pd

        filename = file.name.lower()

        if filename.endswith(".csv"):

            df_sa = pd.read_csv(file)

        else:

            df_sa = pd.read_excel(file)

        st.dataframe(
            df_sa.head()
        )

        group = st.selectbox(
            "Grouping variable",
            df_sa.columns
        )

        outcome = st.selectbox(
            "Outcome variable",
            df_sa.columns
        )

        if st.button(
            "Run Analysis"
        ):

            result = run_ttest(
                df_sa,
                group,
                outcome
            )

            st.subheader(
                "Results"
            )

            st.write(
                result
            )

            p_value = result["p-val"].iloc[0]

            st.info(
                interpret_p_value(
                    p_value
                )
            )


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

                st.write(
                    paper["abstract"]
                )

                if st.button(f"Save Paper", key=f"save_{idx}"):

                    save_paper(
                        project_id=1,
                        title=paper["title"],
                        abstract=paper["abstract"]
                    )

                    st.success(
                        "Paper saved"
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

    if st.button("Load Papers"):

        papers = get_papers(
            project_id
        )

        if papers:

            for paper in papers:

                st.subheader(
                    paper.title
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
