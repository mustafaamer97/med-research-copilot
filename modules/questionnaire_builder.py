from ai.llm_engine import ask_ai


def generate_questionnaire(
    research_context=None,
    research_question=None,
    protocol=None
):

    context_text = ""

    if research_context:

        context_text = f"""
Medical Field:
{research_context.get("field", "")}

Disease:
{research_context.get("disease", "")}

Population:
{research_context.get("population", "")}

Location:
{research_context.get("location", "")}

Study Period:
{research_context.get("study_period", "")}

Study Design:
{research_context.get("study_design", "")}

Research Goal:
{research_context.get("research_goal", "")}
"""

    question_text = ""

    pico_text = ""

    if research_question:

        question_text = research_question.get(
            "question",
            ""
        )

        pico = research_question.get(
            "pico",
            {}
        )

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

    prompt = f"""
You are a senior medical epidemiologist and questionnaire design expert.

Create a publication-ready scientific questionnaire.

=================================================
RESEARCH CONTEXT
=================================================

{context_text}

=================================================
RESEARCH QUESTION
=================================================

{question_text}

=================================================
PICO FRAMEWORK
=================================================

{pico_text}

=================================================
RESEARCH PROTOCOL
=================================================

{protocol}

=================================================
INSTRUCTIONS
=================================================

Build the questionnaire directly from the protocol.

Identify:

- Demographic variables
- Clinical variables
- Exposure variables
- Risk factor variables
- Outcome variables
- Confounding variables

If the study is observational:
Use exposure/risk-factor language.

If the study is interventional:
Use intervention language.

Suggest validated scales whenever appropriate.

For each question provide:

- Question text
- Variable name
- Variable type
  (Numeric / Categorical / Binary / Ordinal)
- Suggested coding

=================================================
OUTPUT FORMAT
=================================================

# SECTION 1: DEMOGRAPHICS

Q1:
Variable:
Type:
Coding:

Q2:
Variable:
Type:
Coding:

# SECTION 2: CLINICAL VARIABLES

Q3:
Variable:
Type:
Coding:

# SECTION 3: EXPOSURE / INTERVENTION VARIABLES

Q4:
Variable:
Type:
Coding:

# SECTION 4: OUTCOME VARIABLES

Q5:
Variable:
Type:
Coding:

# SECTION 5: CONFOUNDERS

Q6:
Variable:
Type:
Coding:

# DATA DICTIONARY

Create a complete variable dictionary table.
"""

    try:

        return ask_ai(prompt)

    except Exception as e:

        return f"""
# Questionnaire Generation Error

Unable to generate questionnaire.

Error:
{str(e)}
"""
