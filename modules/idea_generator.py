from ai.llm_engine import ask_ai
from ai.prompts import RESEARCH_IDEA_PROMPT
from modules.evidence_search import get_recent_evidence


def generate_research_ideas(field: str) -> str:
    """
    جلب الأدلة البحثية الحديثة بناءً على المجال المحدد، 
    ثم توليد أفكار بحثية معتمدة على ثغرات المعرفة الموجودة في الأدلة.
    """
    # جلب الأوراق البحثية الحديثة
    papers = get_recent_evidence(field)

    # تجميع نصوص الأدلة البحثية
    evidence_text = ""
    if papers:
        for paper in papers:
            title = paper.get('title', 'No Title')
            abstract = paper.get('abstract', 'No Abstract')
            evidence_text += f"Title: {title}\nAbstract:\n{abstract}\n\n"
    else:
        evidence_text = "No recent PubMed evidence available for this field.\n\n"

    # تجهيز النص الأساسي للـ Prompt
    prompt = RESEARCH_IDEA_PROMPT.format(field=field)

    # دمج الأدلة الحالية مع الطلب النهائي
    final_prompt = f"""
Current evidence from PubMed:

{evidence_text}

Generate research ideas based on knowledge gaps and opportunities identified in the evidence above.

{prompt}
"""

    return ask_ai(final_prompt)
