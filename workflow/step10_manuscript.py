import streamlit as st

from modules.journal_recommender import (
    recommend_journals
)


def render():

    st.header(
        "📄 Manuscript & Journal Finder"
    )

    literature = st.session_state.get(
        "literature_search",
        []
    )

    research_context = st.session_state.get(
        "research_context",
        {}
    )

    field = research_context.get(
        "field",
        ""
    )

    st.info(
        """
Prepare manuscript information and target journals
for publication planning.
"""
    )

    manuscript_title = st.text_input(
        "Manuscript Title"
    )

    if literature:

        recommendations = (
            recommend_journals(
                literature,
                field
            )
        )

        st.subheader(
            "🎯 Recommended Journals"
        )

        for item in recommendations:

            st.info(
                f"""
{item['journal']}

Supporting Papers:
{item['supporting_papers']}
"""
            )

    manuscript_type = st.selectbox(
        "Manuscript Type",
        [
            "Original Research",
            "Systematic Review",
            "Meta-Analysis",
            "Case Report",
            "Case Series",
            "Short Communication",
            "Letter to Editor"
        ]
    )

    target_journal = st.text_input(
        "Target Journal"
    )

    keywords = st.text_area(
        "Manuscript Keywords"
    )

    if st.button(
        "💾 Save Manuscript Plan",
        use_container_width=True,
        type="primary"
    ):

        st.session_state[
            "manuscript_package"
        ] = {
            "title": manuscript_title,
            "type": manuscript_type,
            "journal": target_journal,
            "keywords": keywords
        }

        st.session_state[
            "manuscript_completed"
        ] = True

        st.success(
            "Manuscript plan saved successfully."
        )

    if st.session_state.get(
        "manuscript_package"
    ):

        st.subheader(
            "Current Manuscript Plan"
        )

        st.json(
            st.session_state[
                "manuscript_package"
            ]
        )

    if st.session_state.get(
        "manuscript_completed"
    ):

        st.success(
            "✅ Step 10 Completed"
        )
