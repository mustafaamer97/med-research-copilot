from ai.llm_engine import ask_ai


def generate_ethics_package(
    research_question="",
    study_type="",
    risk_level="",
    informed_consent=True,
    vulnerable_population=False,
    protocol="",
    sample_size_plan=None,
    research_context=None,
    research_gaps=None
):

    sample_size_plan = sample_size_plan or {}
    research_context = research_context or {}
    research_gaps = research_gaps or []

    prompt = f"""
You are a senior IRB reviewer and medical ethics expert.

Prepare a publication-ready ethics package.

====================================
RESEARCH QUESTION
====================================

{research_question}

====================================
STUDY DESIGN
====================================

{study_type}

====================================
RISK LEVEL
====================================

{risk_level}

====================================
RESEARCH CONTEXT
====================================

Disease:
{research_context.get("disease", "")}

Population:
{research_context.get("population", "")}

Outcome:
{research_context.get("outcome", "")}

Location:
{research_context.get("location", "")}

====================================
PROTOCOL
====================================

{protocol}

====================================
SAMPLE SIZE
====================================

Per Group:
{sample_size_plan.get("per_group", "")}

Total Sample:
{sample_size_plan.get("total_sample", "")}

====================================
RESEARCH GAPS
====================================

{chr(10).join(research_gaps)}

====================================
SPECIAL CONDITIONS
====================================

Informed Consent Required:
{informed_consent}

Includes Vulnerable Population:
{vulnerable_population}

====================================
GENERATE
====================================

1. Ethics Approval Summary

2. Ethical Considerations

3. Risk Assessment

4. Participant Protection Plan

5. Informed Consent Requirements

6. Confidentiality and Data Security

7. Vulnerable Population Protection
(only if applicable)

8. Data Storage and Retention Policy

9. Benefits versus Risks Assessment

10. IRB Submission Summary

11. Ethics Checklist

Use professional academic style.
Use markdown headings.
Suitable for IRB submission.
"""

    return ask_ai(prompt)
