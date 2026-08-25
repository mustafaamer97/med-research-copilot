from ai.llm_engine import ask_ai


def generate_protocol(
    research_idea,
    study_type="Clinical Trial",
    research_context=None,
    research_question=None
):

    context_text = ""

    if research_context:

        context_text = f"""
Medical Field:
{research_context.get("field", "")}

Target Population:
{research_context.get("population", "")}

Data Source:
{research_context.get("data_source", "")}

Keywords:
{research_context.get("keywords", "")}
"""

    question_text = ""

    if research_question:

        question_text = f"""
Research Question:
{research_question.get("question", "")}

Search Keywords:
{research_question.get("keywords", "")}
"""

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

20. Expected Impact

21. Potential Limitations

22. Timeline

Requirements:

- Academic style
- Evidence-based methodology
- Suitable for IRB submission
- Suitable for journal publication
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
