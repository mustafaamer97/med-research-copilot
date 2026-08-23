from ai.llm_engine import ask_ai


def generate_protocol(research_idea):

    prompt = f"""

You are a medical research methodology expert.

Create a complete research protocol.

Research idea:
{research_idea}


Include:

1. Title
2. Background
3. Research Question
4. Objectives
5. Study Design
6. Population
7. Inclusion Criteria
8. Exclusion Criteria
9. Outcomes
10. Statistical Analysis Plan

"""

    result = ask_ai(prompt)

    return result
