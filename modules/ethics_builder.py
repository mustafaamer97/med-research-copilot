from ai.llm_engine import ask_ai


def generate_ethics_package(
    research_question,
    study_type,
    risk_level,
    informed_consent,
    vulnerable_population
):

    prompt = f"""
You are an experienced IRB reviewer.

Create a professional ethics package.

Research Question:
{research_question}

Study Type:
{study_type}

Risk Level:
{risk_level}

Informed Consent Required:
{informed_consent}

Includes Vulnerable Population:
{vulnerable_population}

Generate:

1. Ethical Considerations
2. Risk Assessment
3. Participant Protection Plan
4. Informed Consent Requirements
5. Confidentiality & Data Security
6. IRB Submission Summary

Use academic style.
"""

    return ask_ai(prompt)
