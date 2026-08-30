def generate_references(literature, style="Vancouver"):
    references = []
    
    for i, paper in enumerate(literature, start=1):
        # استخراج وتنقيب البيانات بأمان
        authors = paper.get("authors", "Unknown Authors")
        
        title = (
            paper.get("title", "")
            or ""
        )
        journal = (
            paper.get("journal", "")
            or ""
        )
        year = (
            paper.get("year", "")
            or ""
        )
        pmid = str(
            paper.get("pmid", "")
        ).strip()
        
        doi = str(
            paper.get("doi", "")
        ).strip().lower()

        # Skip low-quality or incomplete references
        missing_fields = []
        if not title.strip():
            missing_fields.append("title")
        if not journal.strip():
            missing_fields.append("journal")
        if not str(year).strip():
            missing_fields.append("year")
            
        if missing_fields:
            # يمكنك تسجيل سبب الاستبعاد هنا للـ Quality Control إذا أردت
            continue

        # تنسيق المرجع حسب النمط المطلوبة
        if style == "Vancouver":
            reference = (
                f"[{i}] "
                f"{authors}. "
                f"{title}. "
                f"{journal}. "
                f"{year}."
            )

            if doi:
                reference += f" DOI: {doi}."
            elif pmid:
                reference += f" PMID: {pmid}."

        else:
            reference = (
                f"[{i}] "
                f"{authors}. "
                f"{title}. "
                f"{journal}. "
                f"{year}."
            )

            if doi:
                reference += f" DOI: {doi}."
            elif pmid:
                reference += f" PMID: {pmid}."

        references.append(reference)

    return "\n".join(references)
