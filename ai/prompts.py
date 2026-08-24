"""
PROJECT AI POLICY

AI assists researchers.

AI does not replace researchers.

AI may generate suggestions.

All outputs require human review.

AI must not fabricate:
- References
- DOI
- PMID
- Statistical results
- Clinical recommendations
"""

from ai.system_prompt import SYSTEM_PROMPT

# ==================== Prompts ====================

PAPER_REVIEW_PROMPT = f"""
{SYSTEM_PROMPT}

Analyze ONLY the information available in the paper text.

If information is not available, write:
"Not Reported"

Provide:

1. Study design
2. Research question
3. Population
4. Intervention
5. Outcomes
6. Main findings
7. Strengths
8. Limitations
9. Risk of bias
10. Evidence quality

Paper text:
{{text}}
"""

RESEARCH_IDEA_PROMPT = f"""
{SYSTEM_PROMPT}

Generate 3 realistic and feasible medical research ideas for the field: {{field}}.

Requirements:

- Suitable for beginner researchers.
- Ethical.
- Low-cost if possible.
- Scientifically meaningful.
- Avoid unrealistic assumptions.
- Do not provide references, DOIs, PMIDs, study names, or publication details unless they are supplied in the evidence context.

For each idea provide:

1. Title
2. Research Question
3. PICO Framework
4. Study Design
5. Target Population
6. Sample Size Considerations (Investigator Decision Required)
7. PubMed Search Keywords
8. Scientific Importance
9. Expected Challenges
"""

PROTOCOL_PROMPT = f"""
{SYSTEM_PROMPT}

Create a structured research protocol.

IMPORTANT:
- If information is missing, state:
  'Investigator Decision Required'

Topic:
{{topic}}

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
10. Sample Size Considerations
11. Data Collection
12. Statistical Analysis Plan
13. Ethical Considerations
14. Potential Limitations
"""
