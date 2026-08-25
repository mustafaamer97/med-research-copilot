import streamlit as st


def render_step8():

    st.header(
        "📝 Data Collection Plan"
    )

    variables = st.text_area(
        "Variables to Collect"
    )

    collection_method = st.selectbox(
        "Collection Method",
        [
            "Survey",
            "Hospital Records",
            "Registry",
            "Laboratory Data"
        ]
    )

    if st.button(
        "Save Collection Plan"
    ):

        st.session_state[
            "data_collection_plan"
        ] = {
            "variables": variables,
            "method": collection_method
        }

        st.session_state[
            "data_collection_completed"
        ] = True

        st.success(
            "Data collection plan saved."
        )

    if st.session_state.get(
        "data_collection_completed"
    ):
        st.success(
            "✅ Step 8 Completed"
        )
