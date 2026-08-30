from ai.llm_engine import ask_ai


def generate_questionnaire(
    research_context=None,
    research_question=None,
    protocol=None,
    sample_size_plan=None,
    study_design="",
    research_gaps=None
):

    prompt = f"""
You are a senior medical research methodologist.

Generate a publication-ready data collection questionnaire.

==================================
RESEARCH CONTEXT
==================================

{research_context}

==================================
RESEARCH QUESTION
==================================

{research_question}

==================================
PROTOCOL
==================================

{protocol}

==================================
SAMPLE SIZE PLAN
==================================

{sample_size_plan}

==================================
STUDY DESIGN
==================================

{study_design}

==================================
RESEARCH GAPS
==================================

{research_gaps}

==================================
REQUIREMENTS
==================================

1. Demographics Section
2. Clinical Variables Section
3. Exposure Variables Section
4. Outcome Variables Section
5. Confounders Section
6. Coding Scheme
7. Variable Type
8. Recommended Data Format

Return markdown format.

For every question include:

- Variable Name
- Question Text
- Data Type
- Coding Method
"""

    return ask_ai(prompt)
