import os
import sys
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --- استيراد الدوال باسم صريح ومحدد لكل خطوة ---
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
from workflow.step5_protocol import (
    render as step5_protocol_render
)
from workflow.step6_sample_size import (
    render as step6_render
)
from workflow.step7_irb import (
    render as step7_render
)
from workflow.step8_data_collection import (
    render as step8_render
)
from workflow.step9_statistics import (
    render as step9_render
)
from workflow.step10_proposal import (
    render as step10_render
)
from workflow.step11_manuscript import (
    render as step11_render
)

# --- الأدوات وقاعدة البيانات ---
from database.db import (
    engine
)
from database.models import (
    Base
)
from modules.library import (
    get_papers,
    search_papers
)
from modules.paper_analyzer import (
    analyze_paper
)
from modules.paper_reviewer import (
    review_paper
)
from utils.pdf_tools import (
    extract_text
)

Base.metadata.create_all(
    bind=engine
)

# =========================
# Session State Setup
# =========================
if "research_context" not in st.session_state:
    st.session_state["research_context"] = {}

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
    "proposal_completed": False,
    "manuscript_completed": False,
    "google_form_ready": False,
}

for key, value in WORKFLOW_STEPS.items():
    if key not in st.session_state:
        st.session_state[key] = value

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

# --- القائمة الجانبية ---
st.sidebar.title(
    "🧬 Research Workflow"
)

menu = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",

        "──────── PHASE 1 ────────",
        "Step 1: Research Foundation",
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
        "Step 10: Proposal Builder",
        "Step 11: Manuscript Writer",

        "──────── TOOLS ────────",
        "Research Library",
        "Paper Analyzer"
    ]
)

# --- التنقل والتنفيذ ---

if menu == "🏠 Dashboard":

    st.header(
        "Research Progress"
    )

    progress_items = [

        ("Foundation", st.session_state["context_completed"]),
        ("Idea", st.session_state["idea_completed"]),
        ("Question", st.session_state["question_completed"]),
        ("Literature", st.session_state["literature_completed"]),
        ("Protocol", st.session_state["protocol_completed"]),
        ("Sample Size", st.session_state["sample_size_completed"]),
        ("IRB", st.session_state["irb_completed"]),
        ("Data Collection", st.session_state["data_collection_completed"]),
        ("Statistics", st.session_state["analysis_completed"]),
        ("Proposal", st.session_state["proposal_completed"]),
        ("Manuscript", st.session_state["manuscript_completed"]),
    ]

    completed = sum(
        1 for _, done in progress_items if done
    )

    progress = completed / len(progress_items)

    st.progress(progress)

    for name, done in progress_items:

        if done:

            st.success(
                f"✅ {name}"
            )

        else:

            st.info(
                f"⬜ {name}"
            )

elif menu == "Step 1: Research Foundation":

    step1_render()

elif menu == "Step 2: Idea Generator & Validation":

    step2_render()

elif menu == "Step 3: Research Question Builder":

    step3_render()

elif menu == "Step 4: Literature Search & Analyzer":

    step4_render()

elif menu == "Step 5: Protocol Builder":

    step5_protocol_render()

elif menu == "Step 6: Sample Size & Power":

    step6_render()

elif menu == "Step 7: Ethics & IRB":

    step7_render()

elif menu == "Step 8: Data Collection":

    step8_render()

elif menu == "Step 9: Statistical Analysis":

    step9_render()

elif menu == "Step 10: Proposal Builder":

    step10_render()

elif menu == "Step 11: Manuscript Writer":

    step11_render()

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
