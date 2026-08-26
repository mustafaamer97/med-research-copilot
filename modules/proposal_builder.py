from ai.llm_engine import ask_ai


def generate_proposal(
    research_context=None,
    research_question=None,
    selected_idea=None,
    protocol=None,
    literature=None,
    research_gaps=None
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

Keywords:
{research_context.get('keywords','')}
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

    if literature:

        evidence_summary = "\n".join(
            [
                f"- {paper.get('title','')} ({paper.get('year','')})"
                for paper in literature[:20]
            ]
        )

    gap_text = ""

    if research_gaps:

        gap_text = "\n".join(
            research_gaps
        )

    prompt = f"""
You are a senior academic medical researcher.

Create a complete publication-quality research proposal.

========================
RESEARCH CONTEXT
========================

{context_text}

========================
RESEARCH IDEA
========================

{idea_text}

========================
RESEARCH QUESTION
========================

{question_text}

========================
LITERATURE SUMMARY
========================

{evidence_summary}

========================
RESEARCH GAPS
========================

{gap_text}

========================
PROTOCOL
========================

{protocol}

========================
REQUIREMENTS
========================

Generate:

# Title

# Abstract

# Introduction

# Literature Review

# Research Gap

# Research Question

# Hypothesis

# Objectives

# Methodology

# Study Population

# Inclusion Criteria

# Exclusion Criteria

# Sample Size Considerations

# Data Collection

# Statistical Analysis

# Ethical Considerations

# Expected Results

# Timeline

# References Placeholder

Use academic style suitable for:
- University proposal submission
- IRB submission
- Grant submission

Return markdown format.
"""

    try:

        return ask_ai(prompt)

    except Exception as e:

        return f"""
# Proposal Generation Error

{str(e)}
"""
