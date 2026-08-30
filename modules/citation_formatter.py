import re


def insert_vancouver_citations(
    manuscript,
    literature
):
    """Citations are generated directly by the LLM

    according to the prompt rules.
    No automatic keyword replacement post-processing.
    """
    if not manuscript:
        return manuscript

    if not literature:
        return manuscript

    # اختيارياً: يمكن الاحتفاظ بالتحقق من صحة الأرقام فقط دون تعديل النص
    max_reference = len(literature)
    citations = re.findall(
        r"\[(\d+)\]",
        manuscript
    )

    # التحقق من أن الاستشهادات ضمن نطاق المراجع المتاحة
    for citation in citations:
        num = int(citation)
        if num > max_reference:
            # يمكن تسجيل تنبيه أو تركها للمراجعة
            pass

    return manuscript
