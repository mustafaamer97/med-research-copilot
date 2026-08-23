from ai.llm_engine import ask_ai
from ai.prompts import RESEARCH_IDEA_PROMPT



def generate_research_ideas(field):

    prompt = RESEARCH_IDEA_PROMPT.format(
        field=field
    )

    response = ask_ai(prompt)

    return response
