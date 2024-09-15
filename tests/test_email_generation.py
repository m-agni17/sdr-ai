import unittest

def generate_email(prospect_name, company_name, research_report, product_catalog):
    return f"""
    Dear {prospect_name},

    I hope this message finds you well.

    At {company_name}, we are excited to offer our cutting-edge solutions. Here's what we have gathered about your company:
    - Company Overview: {research_report.get("company_overview", "No data available")}
    - Key Contacts: {research_report.get("key_contacts", "No data available")}
    - Recent News: {research_report.get("recent_news", "No data available")}
    - Industry Trends: {research_report.get("industry_trends", "No data available")}

    Our product catalog includes: {product_catalog}

    Best regards,
    Sales Team
    """

class TestEmailGeneration(unittest.TestCase):
    
    def setUp(self):
        # Sample data for testing
        self.prospect_name = "Arjun"
        self.company_name = "AiShield"
        self.research_report = {
            "company_overview": "Deep learning startup specializing in computer vision.",
            "key_contacts": "Yuvaraj- CTO",
            "recent_news": "Tech Innovations has launched a new AI product.",
            "industry_trends": "AI and machine learning are rapidly evolving fields."
        }
        self.product_catalog = "Our catalog includes advanced AI solutions for various industries."

    def test_generate_email(self):
        # Call the function with test data
        email_draft = generate_email(
            self.prospect_name,
            self.company_name,
            self.research_report,
            self.product_catalog
        )
        
        # Check if the email draft contains the prospect name and company name
        self.assertIn(self.prospect_name, email_draft)
        self.assertIn(self.company_name, email_draft)
        self.assertIn("AI technologies", email_draft)
        self.assertIn("Tech Innovations", email_draft)

if __name__ == "__main__":
    unittest.main()
