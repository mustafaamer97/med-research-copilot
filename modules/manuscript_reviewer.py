from ai.llm_engine import ask_ai


def review_manuscript(
    manuscript,
    protocol=None,
    proposal=None,
    statistics_report=None,
    target_journal=None
):
    """
    Performs a comprehensive medical journal peer review for a manuscript
    using available context (protocol, proposal, stats, target journal).
    """

    # Helper function to format optional context cleanly
    def format_context(label, content):
        if not content:
            return f"=================================\n{label}\n=================================\nNot provided.\n"
        return f"=================================\n{label}\n=================================\n{content}\n"

    target_journal_str = format_context("TARGET JOURNAL", target_journal)
    protocol_str = format_context("PROTOCOL", protocol)
    proposal_str = format_context("PROPOSAL", proposal)
    stats_str = format_context("STATISTICAL REPORT", statistics_report)

    prompt = f"""
You are an expert senior medical journal reviewer and editorial board member.

Review the provided manuscript thoroughly. You are also given additional research context (Protocol, Proposal, Statistical Report, Target Journal) to evaluate consistency and completeness accurately.

{target_journal_str}
{protocol_str}
{proposal_str}
{stats_str}
=================================
MANUSCRIPT TO REVIEW
=================================
{manuscript}

REQUIREMENTS:
Provide a detailed, highly constructive peer review report. Evaluate the manuscript in light of the provided Protocol, Proposal, and Statistical Report (e.g., do not flag missing sample size rationale if it exists in the protocol/stats report).

Provide the exact following markdown sections:

# Overall Assessment

# Reviewer Scores
Provide scores for each of the following (Format: **Metric**: X/10 or X%):
- Novelty Score (1-10)
- Methodology Score (1-10)
- Statistical Quality Score (1-10)
- Clinical Relevance Score (1-10)
- Writing Quality Score (1-10)
- Publication Readiness Score (0-100%)

# Major Strengths

# Major Weaknesses

# Missing Sections

# Methodological Concerns

# Statistical Concerns

# Reporting Guideline Compliance
Identify applicable reporting guideline (e.g., CONSORT for RCTs, STROBE for observational studies, PRISMA for systematic reviews, CARE for case reports, TREND for non-randomized trials) and estimate compliance percentage with key checklist items.

# Journal Fit Analysis
Evaluate whether the manuscript aligns with the target journal's scope, audience, and standards (or provide general target advice if no journal is specified).

# Submission Readiness
State whether the manuscript is ready for:
- Internal Review
- IRB Submission
- Journal Submission

# Actionable Revision Checklist
Provide a prioritized, numbered checklist of specific steps the author must execute to improve the paper.

# Publication Recommendation
Choose exactly one:
- Accept
- Minor Revision
- Major Revision
- Reject

Return markdown formatting only.
"""

    try:
        return ask_ai(prompt)
    except Exception as e:
        return f"""
# Review Error

Failed to generate review. Error details:
{str(e)}
"""
