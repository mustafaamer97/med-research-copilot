class ASReviewAdapter:

    def __init__(self):
        self.name = "ASReview"


    def create_screening_project(
        self,
        papers
    ):

        """
        Send papers to ASReview
        """

        return {
            "status": "ready",
            "papers": len(papers)
        }


    def screen_results(
        self
    ):

        """
        Return included/excluded studies
        """

        return []
