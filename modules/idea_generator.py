import streamlit as st
from ai.llm_engine import ask_ai
from ai.prompts import RESEARCH_IDEA_PROMPT
from modules.evidence_search import get_recent_evidence


def generate_research_ideas(field):

    papers = get_recent_evidence(field)

    evidence_text = ""

    for paper in papers:

        evidence_text += f"""

Title:
{paper['title']}

Abstract:
{paper['abstract']}

"""

    prompt = RESEARCH_IDEA_PROMPT.format(
        field=field
    )

    final_prompt = f"""

Evidence Context:

{evidence_text}

Use the evidence above to identify
knowledge gaps and generate
research ideas.

{prompt}

"""

    # عرض سياق الأدلة على واجهة Streamlit مؤقتاً للمعاينة والتحقق
    st.write(evidence_text)

    return ask_ai(final_prompt)
