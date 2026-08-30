import streamlit as st

from modules.context_manager import get_context, update_context
from modules.docx_exporter import export_to_docx
from modules.journal_recommender import recommend_journals
from modules.manuscript_reviewer import review_manuscript
from modules.manuscript_writer import (
    generate_manuscript,
    revise_manuscript,  # يفترض إضافة دالة التعديل بناءً على التقرير
)


def render():
    st.header("📄 Manuscript Writer & Journal Finder")

    # ==================================
    # 1 & 2. Unified Context Management
    # ==================================
    context = get_context()

    # البيانات الرئيسية من السياق الموحد
    research_context = context.get("research_context", {})
    research_question = context.get("research_question", {})
    selected_idea = context.get("selected_research_idea", {})
    protocol = context.get("research_protocol", "")
    proposal = context.get("research_proposal", "")
    literature = context.get("literature_search", [])

    # إحصائيات الخطوات 9 و 10
    statistics_results = context.get("statistics_results")
    statistics_test = context.get("statistics_test", "")
    statistics_report = context.get("statistics_report", "")

    # بيانات الخطوات 6 إلى 8 المهمة للتكامل الشامل
    sample_size_plan = research_context.get("sample_size_plan", {})
    data_collection_plan = research_context.get("data_collection_plan", {})
    ethics_summary = research_context.get("ethics_summary", {})
    data_dictionary = research_context.get("data_dictionary", [])

    field = research_context.get("field", "Medicine")
    study_design = research_context.get("study_design", "Observational")

    # ==================================
    # 4. Publication Readiness Score
    # ==================================
    manuscript_existing = st.session_state.get("research_manuscript")

    score = 0
    if proposal:
        score += 20
    if protocol:
        score += 20
    if statistics_results:
        score += 30
    if literature:
        score += 20
    if manuscript_existing:
        score += 10

    st.subheader("📊 Publication Readiness")
    st.progress(score / 100)
    st.metric("Readiness Score", f"{score}%")

    st.divider()

    # ==================================
    # 6. Enhanced Statistics Status
    # ==================================
    st.subheader("Statistical Analysis Status")

    if statistics_results is not None:
        st.success(
            f"""
**Statistics Available**  
* **Test:** {statistics_test}  
* **Results Ready:** Yes
"""
        )
    else:
        st.warning(
            "No statistical analysis found. The manuscript can still be generated, "
            "but the Results section will be descriptive or limited."
        )

    # ==================================
    # 3 & 7. Journal Recommendation & Target Selection
    # ==================================
    if literature:
        st.subheader("🎯 Recommended Journals")

        # التوصية باستخدام Study Design و Field لدقة أعلى
        journals = recommend_journals(
            literature=literature,
            field=field,
            study_design=study_design
        )

        journal_names = [j.get("journal", "Unknown") for j in journals] if journals else []

        if journal_names:
            selected_journal = st.selectbox(
                "Select Target Journal",
                options=journal_names,
                help="This selection will format the manuscript & cover letter according to the target journal."
            )

            # حفظ المجلة المختارة في session_state و context
            st.session_state["target_journal"] = selected_journal
            update_context({"target_journal": selected_journal})

        for item in journals:
            st.info(
                f"""
**Journal:** {item.get('journal', 'N/A')}  
**Supporting Papers:** {item.get('supporting_papers', 'N/A')}
"""
            )

    st.divider()

    # ==================================
    # 5. Generate Manuscript (with validations)
    # ==================================
    st.subheader("📝 Generate Manuscript")

    if st.button("📄 Generate Full Manuscript", use_container_width=True, type="primary"):
        # التحقق من وجود الشروط الأساسية لتجنب التوليد الفارغ
        if not protocol:
            st.error("❌ Protocol must be generated first (Step 4/5).")
            st.stop()

        if not proposal:
            st.error("❌ Proposal must be generated first.")
            st.stop()

        with st.spinner("Writing full manuscript using comprehensive research context..."):
            manuscript = generate_manuscript(
                research_context=research_context,
                research_question=research_question,
                selected_idea=selected_idea,
                protocol=protocol,
                proposal=proposal,
                literature=literature,
                statistics_results=statistics_report,
                sample_size_plan=sample_size_plan,
                data_collection_plan=data_collection_plan,
                ethics_summary=ethics_summary,
                data_dictionary=data_dictionary,
                target_journal=st.session_state.get("target_journal", "")
            )

        st.session_state["research_manuscript"] = manuscript
        st.session_state["manuscript_completed"] = True
        update_context({"research_manuscript": manuscript})

        st.rerun()

    # ==================================
    # Display & Review & Revise Manuscript
    # ==================================
    manuscript = st.session_state.get("research_manuscript")

    if manuscript:
        st.subheader("Generated Manuscript")
        st.markdown(manuscript)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Review Manuscript", use_container_width=True):
                with st.spinner("Reviewing manuscript..."):
                    review = review_manuscript(manuscript)

                st.session_state["manuscript_review"] = review
                update_context({"manuscript_review": review})
                st.rerun()

        # ==================================
        # 8. Revise Manuscript Action
        # ==================================
        review_report = st.session_state.get("manuscript_review")

        with col2:
            if review_report:
                if st.button("🔄 Revise Manuscript (Apply Feedback)", use_container_width=True, type="secondary"):
                    with st.spinner("Revising manuscript based on peer review recommendations..."):
                        revised_manuscript = revise_manuscript(
                            manuscript=manuscript,
                            review=review_report
                        )

                    st.session_state["research_manuscript"] = revised_manuscript
                    update_context({"research_manuscript": revised_manuscript})
                    st.success("Manuscript successfully revised!")
                    st.rerun()

        # التصدير والتحميل
        st.download_button(
            "⬇️ Download Manuscript (.md)",
            data=manuscript,
            file_name="research_manuscript.md",
            use_container_width=True
        )

        docx_file = export_to_docx(
            manuscript,
            "Research Manuscript",
            "research_manuscript.docx"
        )

        with open(docx_file, "rb") as file:
            st.download_button(
                "⬇️ Download Manuscript (.docx)",
                data=file,
                file_name="research_manuscript.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

    # ==================================
    # Display Peer Review Report
    # ==================================
    review = st.session_state.get("manuscript_review")

    if review:
        st.subheader("📋 Peer Review Report")
        st.markdown(review)

        st.download_button(
            "⬇️ Download Peer Review (.md)",
            data=review,
            file_name="peer_review_report.md",
            use_container_width=True
        )

    # ==================================
    # Completion Banner
    # ==================================
    if st.session_state.get("manuscript_completed"):
        st.success("✅ Step 11 Completed: Manuscript Ready for Final Review & Submission")
