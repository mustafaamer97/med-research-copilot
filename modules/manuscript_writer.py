from ai.llm_engine import (
    ask_ai
)
from modules.citation_formatter import (
    insert_vancouver_citations
)
from modules.reference_generator import (
    generate_references
)


def truncate_text(text, max_chars=15000):
    if not text:
        return ""
    return str(text)[:max_chars]


def generate_manuscript(
    research_context=None,
    research_question=None,
    selected_idea=None,
    protocol=None,
    proposal=None,
    data_collection_plan=None,
    literature=None,
    statistics_results=None,
    statistics_report=None,
    statistics_test=None,
    sample_size_plan=None,
    ethics_summary=None,
    target_journal=None,
):

    proposal = truncate_text(proposal)
    protocol = truncate_text(protocol)
    statistics_report = truncate_text(statistics_report)

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

    journal_text = (
        target_journal
        if target_journal
        else "General Medical Journal"
    )

    prompt = f"""
You are a senior medical researcher and scientific writer.

Write a complete publication-ready medical manuscript.

=================================
TARGET JOURNAL
=================================

{journal_text}

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
DATA COLLECTION PLAN
=================================

{data_collection_plan}

=================================
SAMPLE SIZE PLAN
=================================

{sample_size_plan}

=================================
ETHICS SUMMARY
=================================

{ethics_summary}

=================================
LITERATURE
=================================

{evidence_summary}

=================================
STATISTICAL TEST USED
=================================

{statistics_test}

=================================
RAW STATISTICAL RESULTS
=================================

{statistics_results}

=================================
STATISTICAL REPORT
=================================

{statistics_report}

=================================
REFERENCES
=================================

{references_text}

=================================
REQUIREMENTS
=================================

Identify the appropriate reporting guideline (CONSORT, STROBE, PRISMA, CARE) based on the study design and structure the manuscript accordingly.

For systematic reviews and meta-analyses:
- Do not generate patient-level results.
For observational studies:
- Follow STROBE structure.
For randomized trials:
- Follow CONSORT structure.
For case reports:
- Follow CARE structure.

Generate:

# Title

# Abstract

Structured:
- Background
- Methods
- Results
- Conclusion

# Keywords

# Plain Language Summary

# Introduction

# Methods

Include:
- Study Design
- Setting
- Population
- Sample Size
- Data Collection
- Statistical Analysis
- Ethics Approval

# Results

Include:
- Descriptive Statistics
- Main Findings
- Effect Sizes
- Confidence Intervals
- P-values

# Discussion

# Clinical Implications

# Strengths

# Limitations

# Future Research

# Conclusion

# Submission Checklist

Provide a checklist indicating:
- Title complete
- Abstract complete
- Methods complete
- Statistical analysis complete
- Ethics statement complete
- References complete
Mark each item as:
✓ Complete
△ Needs Revision
✗ Missing

# References

Additional Requirements:

- Academic writing style suitable for medical publication.
- Follow appropriate reporting guideline (CONSORT/STROBE/PRISMA/CARE).
- Integrate protocol, proposal, data collection plan, and ethics summary consistently.
- If statistical results are missing, explicitly state that no statistical analysis has been performed yet.
- Never fabricate: Sample sizes, Means, Standard deviations, Confidence intervals, P-values, Effect sizes.
- Use statistical results exactly as supplied; do not invent data or statistical values.
- Results section must describe effect sizes, confidence intervals, p-values, and statistical findings clearly.
- Discussion must interpret findings clinically.
- Journal-ready format.

IMPORTANT CITATION RULES:

- Use numbered in-text citations.
- Cite references as [1], [2], [3] inside the manuscript.
- Every major scientific claim should have a citation.
- Use only the supplied references.
- Do not invent references.
- Keep reference numbering exactly as provided.
- Include citations throughout Introduction, Discussion and Conclusion when appropriate.

Example:

Hypertension remains a major public health problem [1].
Several randomized trials demonstrated improved outcomes [2,3].
Recent systematic reviews confirmed these findings [4].

Return markdown only.
"""

    try:
        manuscript = ask_ai(prompt)

        if literature and manuscript:
            manuscript = insert_vancouver_citations(
                manuscript,
                literature
            )

        if references_text and manuscript:
            if "# References" not in manuscript:
                manuscript += (
                    "\n\n# References\n\n"
                    + references_text
                )

        return manuscript

    except Exception as e:
        return f"""
# Manuscript Generation Error

{str(e)}
"""
