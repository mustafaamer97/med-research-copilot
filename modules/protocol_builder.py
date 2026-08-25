from ai.llm_engine import ask_ai

from modules.protocol_context_builder import (
    build_protocol_context
)


def generate_protocol(
    research_idea="",
    study_type="Clinical Trial"
):

    protocol_context = (
        build_protocol_context()
    )

    research_context = (
        protocol_context.get(
            "context",
            {}
        )
    )

    idea = (
        protocol_context.get(
            "idea",
            {}
        )
    )

    question = (
        protocol_context.get(
            "question",
            {}
        )
    )

    evidence = (
        protocol_context.get(
            "evidence",
            []
        )
    )

    prompt = f"""
You are a senior medical researcher,
clinical epidemiologist,
and biostatistician.

Build a complete academic research protocol.

=================================================
RESEARCH CONTEXT
=================================================

Medical Field:
{research_context.get("field","")}

Target Population:
{research_context.get("population","")}

Study Design:
{research_context.get("study_design","")}

Data Source:
{research_context.get("data_source","")}

Keywords:
{research_context.get("keywords","")}

=================================================
RESEARCH IDEA
=================================================

Title:
{idea.get("title","")}

Description:
{idea.get("description","")}

=================================================
PICO QUESTION
=================================================

Research Question:
{question.get("question","")}

Search Strategy:
{question.get("keywords","")}

=================================================
BEST AVAILABLE EVIDENCE
=================================================

{chr(10).join(evidence)}

=================================================
REQUEST
=================================================

Generate a professional research protocol.

Include:

1. Protocol Title

2. Background and Rationale

3. Literature Gap

4. Research Question

5. Hypothesis

6. Primary Objective

7. Secondary Objectives

8. Study Design

9. Study Setting

10. Study Population

11. Inclusion Criteria

12. Exclusion Criteria

13. Sample Size Considerations

14. Data Collection Plan

15. Variables

16. Primary Outcome

17. Secondary Outcomes

18. Statistical Analysis Plan

19. Bias Reduction Strategy

20. Ethical Considerations

21. Expected Impact

22. Future Research Directions

Write using academic medical research style.

Use the provided evidence whenever possible.

Avoid generic text.
"""

    result = ask_ai(prompt)

    return result
