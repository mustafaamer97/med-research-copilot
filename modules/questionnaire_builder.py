from ai.llm_engine import ask_ai


def generate_questionnaire(
    research_context=None,
    research_question=None,
    protocol=None
):

    prompt = f"""
You are an expert medical researcher.

Generate a scientific questionnaire based on:

Research Context:
{research_context}

Research Question:
{research_question}

Protocol:
{protocol}

Requirements:

1. Identify important variables.
2. Generate demographic questions.
3. Generate study-specific questions.
4. Suggest validated scales when appropriate.
5. Return the questionnaire in structured format.

Format:

SECTION 1: Demographics

Q1:
Q2:

SECTION 2: Clinical Variables

Q3:
Q4:

SECTION 3: Outcome Variables

Q5:
Q6:
"""

    return ask_ai(prompt)
