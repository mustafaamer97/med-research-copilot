def analyze_paper(text):

    sections = {

        "Objective": "",
        "Methods": "",
        "Results": "",
        "Limitations": ""

    }


    lower_text = text.lower()


    if "objective" in lower_text:

        sections["Objective"] = extract_section(
            text,
            "objective"
        )


    if "method" in lower_text:

        sections["Methods"] = extract_section(
            text,
            "method"
        )


    if "result" in lower_text:

        sections["Results"] = extract_section(
            text,
            "result"
        )


    if "limitation" in lower_text:

        sections["Limitations"] = extract_section(
            text,
            "limitation"
        )


    return sections



def extract_section(text, keyword):

    start = text.lower().find(keyword)

    return text[start:start+1000]
