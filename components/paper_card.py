import streamlit as st
from modules.library import save_paper


def render_paper_card(paper, index):
    """
    Renders an individual paper card UI with details and a save button.
    """
    title = paper.get("title", "No Title")
    journal = paper.get("journal", "Unknown Journal")
    year = paper.get("year", "N/A")
    evidence = paper.get("evidence_level", "Unknown")
    doi = paper.get("doi", "")
    abstract = paper.get("abstract", "No abstract available.")
    authors = paper.get("authors", "")
    url = paper.get("url", "")
    source = paper.get("source", "Unknown")
    citation_count = paper.get("citation_count", 0)

    with st.container():
        st.markdown("---")
        st.markdown(f"### 📄 {title}")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Year", year)
        with m2:
            st.metric("Evidence", evidence)
        with m3:
            st.metric("Source", source)
        with m4:
            st.metric("Citations", citation_count)

        st.caption(f"Journal: {journal}")
        if authors:
            st.caption(f"Authors: {authors}")
        if doi:
            st.caption(f"DOI: {doi}")

        with st.expander("📖 Abstract"):
            st.write(abstract)

        btn1, btn2 = st.columns(2)
        with btn1:
            if url:
                st.link_button("🔗 Open Article", url)

        with btn2:
            if st.button("💾 Save Paper", key=f"save_{index}"):
                result = save_paper(project_id=1, paper=paper)
                if result.get("saved", False):
                    st.success(result.get("message", "Saved successfully."))
                else:
                    st.warning(result.get("message", "Failed to save."))
