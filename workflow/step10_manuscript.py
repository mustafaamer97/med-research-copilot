import streamlit as st


def render_step10():

    st.header(
        "📄 Manuscript & Journal Finder"
    )

    manuscript_title = st.text_input(
        "Manuscript Title"
    )

    target_journal = st.text_input(
        "Target Journal"
    )

    if st.button(
        "Save Manuscript Plan"
    ):

        st.session_state[
            "manuscript_package"
        ] = {
            "title": manuscript_title,
            "journal": target_journal
        }

        st.session_state[
            "manuscript_completed"
        ] = True

        st.success(
            "Manuscript plan saved."
        )

    if st.session_state.get(
        "manuscript_completed"
    ):
        st.success(
            "✅ Step 10 Completed"
        )
