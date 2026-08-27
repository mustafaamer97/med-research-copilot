import os
import sys
import streamlit as st


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


# ==================================
# Workflow Imports
# ==================================

from workflow.step1_field import (
    render as step1_render
)

from workflow.step2_idea import (
    render as step2_render
)

from workflow.step3_question import (
    render as step3_render
)

from workflow.step4_literature import (
    render as step4_render
)

from workflow.step5_screening_extraction import (
    render as step5_render
)

from workflow.step6_protocol import (
    render as step6_render
)

from workflow.step7_sample_size import (
    render as step7_render
)

from workflow.step8_irb import (
    render as step8_render
)

from workflow.step9_data_collection import (
    render as step9_render
)

from workflow.step10_statistics import (
    render as step10_render
)

from workflow.step11_proposal import (
    render as step11_render
)

from workflow.step12_manuscript import (
    render as step12_render
)


# ==================================
# Database
# ==================================

from database.db import engine
from database.models import Base


from modules.library import (
    get_papers,
    search_papers
)

from modules.paper_analyzer import (
    analyze_paper
)

from utils.pdf_tools import (
    extract_text
)


Base.metadata.create_all(
    bind=engine
)


# ==================================
# Session State
# ==================================

DEFAULT_STATES = {

    "research_context": {},

    "context_completed": False,

    "idea_completed": False,

    "question_completed": False,

    "literature_completed": False,

    "screening_completed": False,

    "protocol_completed": False,

    "sample_size_completed": False,

    "irb_completed": False,

    "data_collection_completed": False,

    "analysis_completed": False,

    "proposal_completed": False,

    "manuscript_completed": False,

}


for key, value in DEFAULT_STATES.items():

    if key not in st.session_state:

        st.session_state[key] = value



# ==================================
# Page Config
# ==================================

st.set_page_config(

    page_title="Med Research Copilot",

    page_icon="🧬",

    layout="wide"

)



st.title(
    "🧬 Med Research Copilot"
)

st.subheader(
    "AI Assistant for Medical Research"
)



# ==================================
# Sidebar
# ==================================

st.sidebar.title(
    "🧬 Research Workflow"
)



menu = st.sidebar.radio(

    "Navigate",

    [

        "🏠 Dashboard",


        "──────── PHASE 1 ────────",

        "Step 1: Context & Scope Builder",

        "Step 2: Idea Generator & Validation",

        "Step 3: Research Question Builder",


        "──────── PHASE 2 ────────",

        "Step 4: Literature Search",

        "Step 5: Screening & Evidence Extraction",

        "Step 6: Protocol Builder",


        "──────── PHASE 3 ────────",

        "Step 7: Sample Size & Power",

        "Step 8: Ethics & IRB",


        "──────── PHASE 4 ────────",

        "Step 9: Data Collection",


        "──────── PHASE 5 ────────",

        "Step 10: Statistical Analysis",


        "──────── PHASE 6 ────────",

        "Step 11: Proposal Builder",

        "Step 12: Manuscript Writer",


        "──────── TOOLS ────────",

        "Research Library",

        "Paper Analyzer"

    ]

)



# ==================================
# Navigation
# ==================================


if menu == "🏠 Dashboard":

    st.write(
        """
Welcome to Med Research Copilot.

Research Workflow:

1. Context & Scope
2. Research Idea
3. Research Question
4. Literature Search
5. Screening & Evidence Extraction
6. Protocol Development
7. Sample Size Calculation
8. Ethics & IRB
9. Data Collection
10. Statistical Analysis
11. Proposal Development
12. Manuscript Writing
"""
    )


elif menu == "Step 1: Context & Scope Builder":

    step1_render()



elif menu == "Step 2: Idea Generator & Validation":

    step2_render()



elif menu == "Step 3: Research Question Builder":

    step3_render()



elif menu == "Step 4: Literature Search":

    step4_render()



elif menu == "Step 5: Screening & Evidence Extraction":

    step5_render()



elif menu == "Step 6: Protocol Builder":

    step6_render()



elif menu == "Step 7: Sample Size & Power":

    step7_render()



elif menu == "Step 8: Ethics & IRB":

    step8_render()



elif menu == "Step 9: Data Collection":

    step9_render()



elif menu == "Step 10: Statistical Analysis":

    step10_render()



elif menu == "Step 11: Proposal Builder":

    step11_render()



elif menu == "Step 12: Manuscript Writer":

    step12_render()



# ==================================
# Research Library
# ==================================


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


    if st.button(
        "Load Papers"
    ):


        papers = (

            search_papers(

                project_id,

                search_term

            )

            if search_term

            else get_papers(

                project_id

            )

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
                "No saved papers."
            )



# ==================================
# Paper Analyzer
# ==================================


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


            text = extract_text(
                file
            )


            analysis = analyze_paper(
                text
            )


        for key, value in analysis.items():

            st.markdown(
                f"### {key}"
            )

            st.write(
                value
            )
