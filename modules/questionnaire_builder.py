from ai.llm_engine import ask_ai


def generate_questionnaire(
    research_context=None,
    research_question=None,
    protocol=None,
    sample_size_plan=None,
    study_design="",
    research_gaps=None,
    data_dictionary=None,
):
    # 1. حماية القيم الفارغة وضمان نوع البيانات المناسب
    research_context = research_context or {}
    research_question = research_question or {}
    sample_size_plan = sample_size_plan or {}
    research_gaps = research_gaps or []
    protocol = protocol or ""
    data_dictionary = data_dictionary or {}

    # 2. تحويل قائمة الفجوات البحثية إلى نص منسق على شكل نقاط
    gaps_text = (
        "\n".join(f"- {gap}" for gap in research_gaps)
        if research_gaps
        else "None specified"
    )

    prompt = f"""
You are a senior medical research methodologist.

Generate a publication-ready data collection questionnaire / Case Report Form (CRF).

==================================
RESEARCH CONTEXT
==================================
{research_context}

==================================
RESEARCH QUESTION
==================================
{research_question}

==================================
PROTOCOL
==================================
{protocol}

==================================
SAMPLE SIZE PLAN
==================================
{sample_size_plan}

==================================
STUDY DESIGN
==================================
{study_design}

==================================
RESEARCH GAPS
==================================
{gaps_text}

==================================
DATA DICTIONARY
==================================
{data_dictionary}

==================================
REQUIREMENTS
==================================
1. Demographics Section
2. Clinical Variables Section
3. Exposure Variables Section
4. Outcome Variables Section
5. Confounders Section
6. Coding Scheme
7. Variable Type
8. Recommended Data Format

Guidelines:
- Use the provided data dictionary whenever available.
- Generate questions directly linked to the listed variables.
- Do not invent unnecessary variables.

For every question, include:
- Variable Name
- Question Text
- Data Type
- Coding Method
- Required (Yes/No)
- Allowed Values
"""

    return ask_ai(prompt)
