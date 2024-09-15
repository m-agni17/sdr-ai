import unittest

def review_email(email_draft, sample_emails):
    feedback = "The email is well-structured but needs more personalization."
    improved_email = f"""
    Dear [Name],

    Our state-of-the-art AI solutions are designed to help companies like [Company] achieve remarkable results. We have personalized this message to suit your needs better:

    {email_draft}

    Sincerely,
    The Team
    """
    
    return {
        "feedback": feedback,
        "improved_email": improved_email
    }

class TestEmailReview(unittest.TestCase):
    
    def setUp(self):
        self.email_draft = """
        Dear Arjun,

        We are excited to offer our cutting-edge AI solutions to Tech Innovations.

        Best regards,
        Sales Team
        """
        
        self.sample_emails = """
        Subject: Enhance Your AI Capabilities with Our Solutions

        Dear [Name],

        Our state-of-the-art AI solutions are designed to help companies like [Company] achieve remarkable results.

        Sincerely,
        The Team
        """

    def test_review_email(self):
        result = review_email(
            self.email_draft,
            self.sample_emails
        )
        self.assertIn("Feedback:", result["feedback"])
        self.assertIn("Improved Email Draft:", result["improved_email"])

if __name__ == "__main__":
    unittest.main()
