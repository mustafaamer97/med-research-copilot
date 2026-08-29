from ai.llm_engine import ask_ai


def generate_protocol(
    research_idea,
    study_type="Clinical Trial",
    research_context=None,
    research_question=None,
    research_gaps=None,
    keywords=None
):

    context_text = ""

    if research_context:

        context_text = f"""
Medical Field:
{research_context.get("field", "")}

Target Population:
{research_context.get("population", "")}

Location:
{research_context.get("location", "")}

Study Period:
{research_context.get("study_period", "")}

Study Design:
{research_context.get("study_design", "")}

Research Goal:
{research_context.get("research_goal", "")}

Data Source:
{research_context.get("data_source", "")}

Evidence Base:
{research_context.get("evidence_count", 0)} studies

Keywords:
{research_context.get("keywords", "")}
"""

    question_text = ""
    pico_text = ""

    if research_question:

        question_text = f"""
Research Question:
{research_question.get("question", "")}

Search Keywords:
{research_question.get("keywords", "")}
"""

        pico = research_question.get("pico", {})

        pico_text = f"""
Population:
{pico.get("population", "")}

Intervention:
{pico.get("intervention", "")}

Comparison:
{pico.get("comparison", "")}

Outcome:
{pico.get("outcome", "")}
"""

    gap_text = ""

    if research_gaps:

        gap_text = "\n".join(
            [
                f"- {gap}"
                for gap in research_gaps
            ]
        )

    keyword_text = ""

    if keywords:

        keyword_text = ", ".join(
            [
                item[0]
                if isinstance(item, (list, tuple))
                else str(item)
                for item in keywords[:10]
            ]
        )

    prompt = f"""
You are a senior medical research methodologist.

Create a publication-ready research protocol.

===================================
RESEARCH IDEA
===================================

{research_idea}

===================================
STUDY TYPE
===================================

{study_type}

===================================
RESEARCH CONTEXT
===================================

{context_text}

===================================
RESEARCH QUESTION
===================================

{question_text}

===================================
PICO FRAMEWORK
===================================

{pico_text}

===================================
DETECTED RESEARCH GAPS
===================================

{gap_text}

===================================
COMMON LITERATURE KEYWORDS
===================================

{keyword_text}

===================================
PROTOCOL REQUIREMENTS
===================================

Generate the protocol using the following sections:

1. Title

2. Background and Rationale

3. Research Question

4. Hypothesis

5. Primary Objective

6. Secondary Objectives

7. Study Design

8. Study Population

9. Inclusion Criteria

10. Exclusion Criteria

11. Recruitment Strategy

12. Sample Size Considerations

13. Data Collection Methods

14. Variables

15. Primary Outcome

16. Secondary Outcomes

17. Statistical Analysis Plan

18. Bias Minimization Strategy

19. Ethical Considerations

20. Research Gap Justification

21. Expected Impact

22. Potential Limitations

23. Timeline

Requirements:

- Academic style
- Evidence-based methodology
- Adapt methodology to the selected study design
- If observational, use exposure/risk-factor language
- If RCT, use intervention language
- Suitable for IRB submission
- Suitable for journal publication
- Explicitly explain how the proposed study addresses the detected research gaps
- Use markdown headings
"""

    try:

        return ask_ai(prompt)

    except Exception as e:

        return f"""
# Protocol Generation Error

Unable to generate protocol.

Error:
{str(e)}
"""
