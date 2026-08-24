from ai.llm_engine import ask_ai


def generate_protocol(
    research_idea,
    study_type="Clinical Trial"
):

    prompt = f"""
You are an expert in medical research methodology.

Create a professional research protocol.

Research Idea:
{research_idea}

Study Type:
{study_type}

Generate the protocol using the following sections:

1. Title

2. Background and Rationale

3. Research Question

4. Primary Objective

5. Secondary Objectives

6. Study Design

7. Study Population

8. Inclusion Criteria

9. Exclusion Criteria

10. Sample Size Considerations

11. Data Collection Methods

12. Primary Outcome

13. Secondary Outcomes

14. Statistical Analysis Plan

15. Ethical Considerations

16. Expected Impact

Write the protocol in a professional academic style.
"""

    result = ask_ai(prompt)

    return result
