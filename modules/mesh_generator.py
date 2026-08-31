import re


MESH_MAP = {

    "smoking": [
        '"Smoking"[Mesh]',
        '"Tobacco Use"[Mesh]'
    ],

    "lung cancer": [
        '"Lung Neoplasms"[Mesh]'
    ],

    "breast cancer": [
        '"Breast Neoplasms"[Mesh]'
    ],

    "diabetes": [
        '"Diabetes Mellitus"[Mesh]'
    ],

    "hypertension": [
        '"Hypertension"[Mesh]'
    ],

    "obesity": [
        '"Obesity"[Mesh]'
    ],

    "mortality": [
        '"Mortality"[Mesh]'
    ],

    "survival": [
        '"Survival Rate"[Mesh]'
    ],

    "risk factor": [
        '"Risk Factors"[Mesh]'
    ]
}


def generate_mesh_terms(text):

    if not text:
        return []

    text = text.lower()

    mesh_terms = []

    for keyword, terms in MESH_MAP.items():

        if keyword in text:

            mesh_terms.extend(
                terms
            )

    return list(
        dict.fromkeys(mesh_terms)
    )


def build_pubmed_query(
    keywords,
    free_text=""
):

    query_parts = []

    for keyword in keywords:

        query_parts.append(
            f'("{keyword}")'
        )

    mesh_terms = generate_mesh_terms(
        free_text
    )

    query_parts.extend(
        mesh_terms
    )

    return " AND ".join(
        query_parts
    )
