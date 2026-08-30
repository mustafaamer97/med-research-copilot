def generate_references(literature, style="Vancouver"):
    references = []
    seen = set()
    reference_number = 1
    
    for paper in literature:
        # استخراج وتنقيب البيانات بأمان
        authors = paper.get("authors", "Unknown Authors")
        if isinstance(authors, list):
            # أخذ أول 6 مؤلفين وإضافة et al إذا تجاوزت القائمة ذلك
            authors_list = [str(a).strip() for a in authors if str(a).strip()]
            if len(authors_list) > 6:
                authors = ", ".join(authors_list[:6]) + " et al"
            elif authors_list:
                authors = ", ".join(authors_list)
            else:
                authors = "Unknown Authors"
        
        title = str(
            paper.get("title", "")
        ).strip()
        
        journal = str(
            paper.get("journal", "")
        ).strip()
        
        year = str(
            paper.get("year", "")
        ).strip()
        
        pmid = str(
            paper.get("pmid", "")
        ).strip()
        
        doi = str(
            paper.get("doi", "")
        ).strip().lower()

        # 1. إزالة المراجع المكررة (بناءً على DOI أو العنوان)
        unique_key = doi if doi else title.lower()
        if not unique_key or unique_key in seen:
            continue
        seen.add(unique_key)

        # 2. استبعاد المراجع الناقصة أو منخفضة الجودة
        if not title:
            continue
        if not journal:
            continue
        if not year:
            continue

        # 3. بناء نص المرجع (يمكن توسيع الـ style مستقبلاً لإضافة APA أو Harvard)
        reference = (
            f"[{reference_number}] "
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
        reference_number += 1

    return "\n".join(references)
