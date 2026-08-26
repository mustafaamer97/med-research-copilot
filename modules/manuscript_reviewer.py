from ai.llm_engine import ask_ai


def review_manuscript(
    manuscript
):

    prompt = f"""
You are a senior medical journal reviewer.

Review the following manuscript.

Provide:

# Overall Assessment

# Major Strengths

# Major Weaknesses

# Missing Sections

# Methodological Concerns

# Statistical Concerns

# Reporting Quality

# Publication Recommendation

Choose one:

- Accept
- Minor Revision
- Major Revision
- Reject

=================================
MANUSCRIPT
=================================

{manuscript}

Return markdown only.
"""

    try:

        return ask_ai(prompt)

    except Exception as e:

        return f"""
# Review Error

{str(e)}
"""
