import streamlit as st


def render():

    st.header(
        "📚 Article Screening"
    )

    st.info(
        "Screen retrieved articles before evidence extraction."
    )


    # ==================================
    # Load Literature Results
    # ==================================

    papers = st.session_state.get(
        "literature_search",
        []
    )

    if not papers:

        st.warning(
            "Please complete Step 4 Literature Search first."
        )

        return


    research_question = st.session_state.get(
        "research_question",
        {}
    )


    if research_question:

        st.subheader(
            "Research Question"
        )

        st.info(
            research_question.get(
                "question",
                ""
            )
        )


    st.divider()


    # ==================================
    # Existing Results
    # ==================================

    existing_results = st.session_state.get(
        "screening_results",
        []
    )


    screening_results = []


    included_count = 0
    excluded_count = 0
    maybe_count = 0


    st.subheader(
        "Article Screening"
    )


    # ==================================
    # Article Cards
    # ==================================

    for idx, paper in enumerate(
        papers
    ):

        title = paper.get(
            "title",
            "No Title"
        )

        year = paper.get(
            "year",
            "Unknown"
        )

        journal = paper.get(
            "journal",
            "Unknown"
        )

        evidence = paper.get(
            "evidence_level",
            "Unknown"
        )

        source = paper.get(
            "source",
            "Unknown"
        )

        abstract = paper.get(
            "abstract",
            ""
        )


        with st.container():

            st.markdown("---")

            st.markdown(
                f"### 📄 {title}"
            )


            c1, c2, c3, c4 = st.columns(4)


            c1.metric(
                "Year",
                year
            )

            c2.metric(
                "Evidence",
                evidence
            )

            c3.metric(
                "Source",
                source
            )

            c4.write(
                journal
            )


            with st.expander(
                "Abstract"
            ):

                st.write(
                    abstract
                )


            decision = st.radio(
                "Decision",
                [
                    "Include",
                    "Exclude",
                    "Maybe"
                ],
                key=f"screen_decision_{idx}"
            )


            reason = ""


            if decision == "Exclude":

                reason = st.text_input(
                    "Reason for exclusion",
                    key=f"exclude_reason_{idx}"
                )


            if decision == "Include":

                included_count += 1

            elif decision == "Exclude":

                excluded_count += 1

            else:

                maybe_count += 1


            screening_results.append(
                {
                    "title": title,

                    "pmid": paper.get(
                        "pmid",
                        ""
                    ),

                    "doi": paper.get(
                        "doi",
                        ""
                    ),

                    "decision": decision,

                    "reason": reason,

                    "paper": paper
                }
            )


    st.divider()


    # ==================================
    # Dashboard
    # ==================================

    st.subheader(
        "Screening Summary"
    )


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Total Articles",
        len(papers)
    )

    c2.metric(
        "Include",
        included_count
    )

    c3.metric(
        "Exclude",
        excluded_count
    )

    c4.metric(
        "Maybe",
        maybe_count
    )


    st.divider()


    # ==================================
    # Save Screening
    # ==================================

    if st.button(
        "💾 Save Screening Results",
        use_container_width=True,
        type="primary"
    ):


        included_articles = [

            item["paper"]

            for item in screening_results

            if item["decision"]
            == "Include"

        ]


        st.session_state[
            "screening_results"
        ] = screening_results


        st.session_state[
            "included_articles"
        ] = included_articles


        st.session_state[
            "screening_completed"
        ] = True


        st.success(
            f"Screening saved. {len(included_articles)} articles included."
        )


        st.rerun()



    # ==================================
    # Completion Status
    # ==================================

    if st.session_state.get(
        "screening_completed"
    ):

        st.success(
            "✅ Step 5 Completed"
        )
