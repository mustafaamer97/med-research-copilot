from ai.llm_engine import ask_ai

from modules.reference_generator import (
    generate_references
)


def generate_manuscript(
    research_context=None,
    research_question=None,
    selected_idea=None,
    protocol=None,
    proposal=None,
    literature=None,
    statistics_results=None
):

    context_text = ""

    if research_context:

        context_text = f"""
Medical Field:
{research_context.get('field','')}

Population:
{research_context.get('population','')}

Study Design:
{research_context.get('study_design','')}

Data Source:
{research_context.get('data_source','')}
"""

    question_text = ""

    if research_question:

        question_text = research_question.get(
            "question",
            ""
        )

    idea_text = ""

    if selected_idea:

        idea_text = f"""
Title:
{selected_idea.get('title','')}

Description:
{selected_idea.get('description','')}
"""

    evidence_summary = ""

    references_text = ""

    if literature:

        evidence_summary = "\n".join(
            [
                f"- {paper.get('title','')} ({paper.get('year','')})"
                for paper in literature[:30]
            ]
        )

        references_text = generate_references(
            literature
        )

    prompt = f"""
You are a senior medical researcher and scientific writer.

Write a complete publication-ready medical manuscript.

=================================
RESEARCH CONTEXT
=================================

{context_text}

=================================
RESEARCH IDEA
=================================

{idea_text}

=================================
RESEARCH QUESTION
=================================

{question_text}

=================================
PROPOSAL
=================================

{proposal}

=================================
PROTOCOL
=================================

{protocol}

=================================
LITERATURE
=================================

{evidence_summary}

=================================
STATISTICAL RESULTS
=================================

{statistics_results}

=================================
REFERENCES
=================================

{references_text}

=================================
REQUIREMENTS
=================================

Generate:

# Title

# Abstract

Structured:
- Background
- Methods
- Results
- Conclusion

# Keywords

# Introduction

# Methods

# Results

# Discussion

# Strengths

# Limitations

# Conclusion

# Future Research

# References

Requirements:

- Academic writing style
- Journal-ready format
- Medical research standards
- Use markdown headings
- Results section must describe the statistical findings when available
- Discussion must interpret findings clinically
- Use the supplied references
- Do not invent references
- Keep reference numbering exactly as provided

Return markdown only.
"""

    try:

        return ask_ai(prompt)

    except Exception as e:

        return f"""
# Manuscript Generation Error

{str(e)}
"""
