import streamlit as st

from database.db import engine
from database.models import Base
from modules.pubmed import search_pubmed


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


menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "New Research Project",
        "Literature Search",
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

            for paper in papers:

                st.subheader(
                    paper["title"]
                )

                st.write(
                    paper["abstract"]
                )

                st.divider()

        else:

            st.warning(
                "No papers found"
            )


elif menu == "Paper Analyzer":

    st.header(
        "Scientific Paper Analyzer"
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            "PDF uploaded successfully"
        )
