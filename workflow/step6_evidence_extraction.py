import streamlit as st

from modules.evidence_extraction import (
    save_extraction
)


def render():

    st.header(
        "📋 Evidence Extraction Workspace"
    )

    st.info(
        """
Extract structured evidence from selected studies.
This information will be used for synthesis and protocol development.
"""
    )

    # ==================================
    # Verification & Load Included Articles
    # ==================================

    if not st.session_state.get(
        "screening_completed",
        False
    ):

        st.warning(
            "Please complete Step 5 screening first."
        )

        return


    articles = st.session_state.get(
        "included_articles",
        []
    )


    if not articles:

        st.warning(
            """
No included studies found.

Please complete Step 5 screening first.
"""
        )

        return


    st.success(
        f"{len(articles)} studies available for extraction."
    )


    # ==================================
    # Select Article
    # ==================================

    titles = [
        article.get(
            "title",
            "Unknown title"
        )
        for article in articles
    ]


    selected_index = st.selectbox(
        "Select Study",
        range(len(titles)),
        format_func=lambda x: titles[x]
    )


    article = articles[selected_index]


    st.divider()


    st.subheader(
        "Study Information"
    )


    st.write(
        article.get(
            "title",
            ""
        )
    )


    st.caption(
        f"""
Year: {article.get('year','')}

Journal: {article.get('journal','')}

Evidence Level:
{article.get('evidence_level','Unknown')}
"""
    )


    # ==================================
    # Extraction Form
    # ==================================

    st.subheader(
        "Evidence Extraction"
    )


    population = st.text_area(
        "Population",
        height=100
    )


    intervention = st.text_area(
        "Intervention / Exposure",
        height=100
    )


    comparator = st.text_area(
        "Comparator",
        height=100
    )


    outcome = st.text_area(
        "Outcome",
        height=100
    )


    study_design = st.selectbox(
        "Study Design",
        [
            "RCT",
            "Cohort",
            "Case-Control",
            "Cross-Sectional",
            "Diagnostic Study",
            "Systematic Review",
            "Meta-analysis",
            "Other"
        ]
    )


    risk_of_bias = st.selectbox(
        "Risk of Bias",
        [
            "Low",
            "Moderate",
            "High",
            "Unclear"
        ]
    )


    notes = st.text_area(
        "Notes",
        height=120
    )


    # ==================================
    # Save Extraction
    # ==================================

    if st.button(
        "💾 Save Evidence Extraction",
        type="primary",
        use_container_width=True
    ):


        extraction = {

            "article_id":
            article.get(
                "pmid",
                ""
            ),

            "doi":
            article.get(
                "doi",
                ""
            ),

            "pmid":
            article.get(
                "pmid",
                ""
            ),

            "population":
            population,

            "intervention":
            intervention,

            "comparator":
            comparator,

            "outcome":
            outcome,

            "study_design":
            study_design,

            "risk_of_bias":
            risk_of_bias,

            "notes":
            notes
        }


        try:

            save_extraction(
                extraction
            )


            st.success(
                "Evidence extraction saved."
            )


            st.session_state[
                "evidence_extraction_completed"
            ] = True


        except Exception as e:

            st.error(
                str(e)
            )


    # ==================================
    # Completion
    # ==================================

    if st.session_state.get(
        "evidence_extraction_completed"
    ):

        st.success(
            "✅ Step 6 Completed"
        )
