import streamlit as st
from copy import deepcopy


DEFAULT_CONTEXT = {

    # =========================
    # Workflow State
    # =========================
    "workflow": {
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
    },

    # =========================
    # Step 1
    # =========================
    "disease": "",
    "population": "",
    "location": "",
    "study_period": "",
    "study_design": "",
    "outcome": "",
    "research_goal": "",

    # =========================
    # Step 2
    # =========================
    "selected_research_idea": {},

    # =========================
    # Step 3
    # =========================
    "research_question": "",
    "research_question_data": {},
    "pico": {},
    "master_query": "",

    # =========================
    # Step 4
    # =========================
    "retrieved_papers": [],
    "evidence_count": 0,
    "research_gaps": [],
    "literature_search_completed": False,

    # =========================
    # Step 5
    # =========================
    "research_protocol": "",
    "protocol_completed": False,
    "final_study_design": "",

    # =========================
    # Step 6
    # =========================
    "sample_size_plan": {},
    "sample_size_per_group": 0,
    "total_sample_size": 0,
    "effect_size": 0,
    "alpha": 0.05,
    "power": 0.80,
    "sample_size_completed": False,

    # =========================
    # Step 7
    # =========================
    "ethics_package": "",
    "ethics_summary": {},
    "irb_completed": False,
    "irb_readiness": 0,
    "risk_level": "",
}


# =====================================================
# Core Context
# =====================================================

def get_context():

    current = st.session_state.get(
        "research_context",
        {}
    )

    merged = deepcopy(DEFAULT_CONTEXT)
    merged.update(current)

    return merged


def save_context(context):

    st.session_state["research_context"] = context

    return context


def update_context(**kwargs):

    context = get_context()

    context.update(kwargs)

    save_context(context)

    return context


def reset_context():

    st.session_state["research_context"] = deepcopy(
        DEFAULT_CONTEXT
    )


# =====================================================
# Simple Access Helpers
# =====================================================

def get_value(key, default=None):

    return get_context().get(
        key,
        default
    )


def context_exists(key):

    value = get_context().get(
        key,
        None
    )

    if value is None:
        return False

    if value == "":
        return False

    if value == {}:
        return False

    if value == []:
        return False

    return True


# =====================================================
# Workflow Manager
# =====================================================

def get_workflow():

    return get_context().get(
        "workflow",
        {}
    )


def is_completed(step):

    workflow = get_workflow()

    key = f"{step}_completed"

    if key in workflow:
        return workflow[key]

    return False


def mark_completed(step):

    context = get_context()

    workflow = context.get(
        "workflow",
        {}
    )

    workflow[f"{step}_completed"] = True

    context["workflow"] = workflow

    save_context(context)

    return context


def mark_incomplete(step):

    context = get_context()

    workflow = context.get(
        "workflow",
        {}
    )

    workflow[f"{step}_completed"] = False

    context["workflow"] = workflow

    save_context(context)

    return context
