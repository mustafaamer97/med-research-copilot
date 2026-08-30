import streamlit as st


DEFAULT_CONTEXT = {

    # Step 1
    "disease": "",
    "population": "",
    "location": "",
    "study_period": "",
    "study_design": "",
    "outcome": "",
    "research_goal": "",

    # Step 2
    "selected_research_idea": {},

    # Step 3
    "research_question": "",
    "research_question_data": {},
    "pico": {},
    "master_query": "",

    # Step 4
    "retrieved_papers": [],
    "evidence_count": 0,
    "research_gaps": [],
    "literature_search_completed": False,

    # Step 5
    "research_protocol": "",
    "protocol_completed": False,
    "final_study_design": "",

    # Step 6
    "sample_size_plan": {},
    "sample_size_per_group": 0,
    "total_sample_size": 0,
    "effect_size": 0,
    "alpha": 0.05,
    "power": 0.80,
    "sample_size_completed": False,

    # Step 7
    "ethics_package": "",
    "ethics_summary": {},
    "irb_completed": False,
    "irb_readiness": 0,
    "risk_level": "",

}


def get_context():

    current = st.session_state.get(
        "research_context",
        {}
    )

    return {
        **DEFAULT_CONTEXT,
        **current
    }


def update_context(**kwargs):

    ctx = get_context()

    ctx.update(kwargs)

    st.session_state[
        "research_context"
    ] = ctx

    return ctx


def reset_context():

    st.session_state[
        "research_context"
    ] = DEFAULT_CONTEXT.copy()


def context_exists(key):

    return key in get_context()


def get_value(key, default=None):

    return get_context().get(
        key,
        default
    )
