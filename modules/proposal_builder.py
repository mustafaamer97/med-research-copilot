import json
from ai.llm_engine import ask_ai


def generate_proposal(
    research_context=None,
    research_question=None,
    selected_idea=None,
    protocol=None,
    literature=None,
    research_gaps=None,
    sample_size_plan=None,
    data_collection_plan=None,
    ethics_summary=None,
    data_dictionary=None,
    statistics_plan=None,
    target_journal=None,
):
    """Generates a comprehensive, publication-quality academic research proposal

    integrating data structure, methodological choices, statistical plans, and
    ethical guidelines.
    """

    # 1. Formatting Research Context
    context_text = ""
    if research_context:
        context_text = f"""
Medical Field:
{research_context.get('field', '')}

Population:
{research_context.get('population', '')}

Study Design:
{research_context.get('study_design', '')}

Data Source:
{research_context.get('data_source', '')}

Keywords:
{research_context.get('keywords', '')}
"""

    # 2. Research Question & Idea
    question_text = ""
    if research_question:
        question_text = research_question.get("question", "")

    idea_text = ""
    if selected_idea:
        idea_text = f"""
Title:
{selected_idea.get('title', '')}

Description:
{selected_idea.get('description', '')}
"""

    # 3. Literature Summary (Optimized to top 25-30 papers to preserve prompt context budget)
    evidence_summary = ""
    if literature:
        evidence_summary = "\n".join(
            [
                f"- {paper.get('title', '')} ({paper.get('year', '')})"
                for paper in literature[:30]
            ]
        )

    # 4. Research Gaps
    gap_text = ""
    if research_gaps:
        gap_text = "\n".join(research_gaps)

    # 5. Serialization of Structured Plans via JSON for Better LLM Parsing
    sample_size_text = json.dumps(sample_size_plan or {}, indent=2)
    data_collection_text = json.dumps(data_collection_plan or {}, indent=2)
    ethics_text = json.dumps(ethics_summary or {}, indent=2)
    data_dict_text = json.dumps(data_dictionary or [], indent=2)
    stats_text = json.dumps(statistics_plan or {}, indent=2)
    journal_text = str(target_journal or "Standard Academic / IRB Submission")

    # 6. Constructing Prompt
    prompt = f"""
You are a senior academic medical researcher and clinical epidemiologist.

Create a complete publication-quality research proposal based strictly on the provided inputs.

========================
RESEARCH CONTEXT
========================
{context_text}

========================
RESEARCH IDEA
========================
{idea_text}

========================
RESEARCH QUESTION
========================
{question_text}

========================
LITERATURE SUMMARY
========================
{evidence_summary}

========================
RESEARCH GAPS
========================
{gap_text}

========================
PROTOCOL
========================
{protocol}

========================
SAMPLE SIZE PLAN (STEP 6)
========================
{sample_size_text}

========================
DATA COLLECTION PLAN (STEP 8)
========================
{data_collection_text}

========================
DATA DICTIONARY (STEP 8)
========================
{data_dict_text}

========================
ETHICAL CONSIDERATIONS SUMMARY (STEP 7)
========================
{ethics_text}

========================
STATISTICAL ANALYSIS PLAN / RESULTS (STEP 9)
========================
{stats_text}

========================
TARGET JOURNAL / AUDIENCE
========================
{journal_text}

========================
REQUIREMENTS & STRUCTURE
========================

IMPORTANT GUIDELINES:
- Use the provided protocol as the primary methodological source. Do not invent a different study design.
- Use the provided statistical analysis plan whenever available.
- Maintain absolute consistency between Research Question, Objectives, Sample Size, Data Collection Plan, Statistical Analysis Plan, and Ethical Considerations.

Generate the proposal in clean Markdown with the following exact sections:

# Title

# Abstract

# Target Journal Alignment
(Explain alignment with {journal_text} scope and formatting)

# Introduction

# Literature Review

# Research Gap

# Research Question

# Hypothesis

# Objectives

# Methodology
Generate sub-sections for:
- Study Design
- Study Setting
- Study Population
- Sampling Strategy
- Sample Size Calculation (incorporate Step 6 plan details)
- Data Collection Procedures (incorporate Step 8 plan details)

# Variables
Derived strictly from the Data Dictionary and methodology:
- Exposure Variables
- Outcome Variables
- Confounders
- Demographic Variables

# Statistical Analysis Plan
Incorporate details from the Step 9 statistical plan:
- Descriptive statistics
- Normality assessment
- Group comparison tests
- Correlation analysis
- Regression analysis
- Significance threshold (α = 0.05)
- Recommended statistical software (e.g., R, SPSS, Python)

# Ethical Considerations
Detail key safeguards based on Step 7 input:
- Risk level assessment
- Informed consent process
- Confidentiality measures
- Data protection strategy
- Vulnerable populations management

# Expected Results & Impact

# Project Timeline
Provide a detailed month-by-month timeline table (Gantt style format).

# References
Generate Vancouver-style citation placeholders strictly based on the provided literature summary.

========================
QUALITY CONTROL CHECKLIST
========================
Before finalizing the proposal, strictly verify:
1. Consistency between study design and statistical plan.
2. Consistency between sample size and methodology.
3. Consistency between variables and outcomes.
4. Consistency between ethics section and risk level.
5. Consistency between timeline and study duration.
If any inconsistencies exist among the provided inputs, explicitly correct them in the text to build a unified proposal.

Style Requirements:
- Formal, high-level academic prose suitable for IRB approval and grant funding.
- Clean Markdown hierarchy.
"""

    try:
        return ask_ai(prompt)
    except Exception as e:
        return f"""
# Proposal Generation Error

An error occurred while communicating with the AI Engine:
{str(e)}
"""
