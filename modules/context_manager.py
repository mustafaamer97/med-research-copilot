def get_context():

    return {
        **{
            "disease": "",
            "population": "",
            "location": "",
            "study_period": "",
            "study_design": "",
            "outcome": "",
        },
        **__import__(
            "streamlit"
        ).session_state.get(
            "research_context",
            {}
        )
    }


def update_context(**kwargs):

    import streamlit as st

    ctx = st.session_state.get(
        "research_context",
        {}
    )

    ctx.update(kwargs)

    st.session_state[
        "research_context"
    ] = ctx
