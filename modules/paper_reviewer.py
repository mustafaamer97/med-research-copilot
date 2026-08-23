from ai.llm_engine import ask_ai
from ai.prompts import PAPER_REVIEW_PROMPT


def review_paper(text):

    prompt = PAPER_REVIEW_PROMPT.format(
        text=text[:12000]
    )

    result = ask_ai(prompt)

    return result
