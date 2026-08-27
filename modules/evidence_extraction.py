from datetime import datetime

from database.db import SessionLocal

from database.models import EvidenceExtraction


def save_extraction(data):

    session = SessionLocal()

    try:

        extraction = EvidenceExtraction(

            article_id=data.get(
                "article_id"
            ),

            doi=data.get(
                "doi"
            ),

            pmid=data.get(
                "pmid"
            ),

            population=data.get(
                "population"
            ),

            intervention=data.get(
                "intervention"
            ),

            comparator=data.get(
                "comparator"
            ),

            outcome=data.get(
                "outcome"
            ),

            study_design=data.get(
                "study_design"
            ),

            risk_of_bias=data.get(
                "risk_of_bias"
            ),

            notes=data.get(
                "notes"
            ),

            updated_at=datetime.utcnow()

        )

        session.add(
            extraction
        )

        session.commit()

        return {
            "saved": True,
            "message": "Extraction saved successfully."
        }


    except Exception as e:

        session.rollback()

        return {
            "saved": False,
            "message": str(e)
        }


    finally:

        session.close()
