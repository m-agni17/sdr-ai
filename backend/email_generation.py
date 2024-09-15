from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Define the prompt template
template = """
Create a personalized email for a Sales Development Representative.and i should not add any changes it should be like i am drafting the mail.

Prospect Name: {prospect_name}
Company Name: {company_name}

add company name and prospect name in the email draft.

Research Report:
Company Overview: {company_overview}
Recent News: {recent_news}
Industry Trends: {industry_trends}

Product Catalog: {product_catalog}


Email Draft:

Hi {prospect_name},

Best regards,
Agni Prasanth,
Sales Development Representative



"""

model = OllamaLLM(model="llama3.1")

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def generate_email(prospect_name, company_name, research_report, product_catalog):
    formatted_report = {
        "company_overview": research_report.get("company_overview", "No data available"),
        "key_contacts": research_report.get("key_contacts", "No data available"),
        "recent_news": research_report.get("recent_news", "No data available"),
        "industry_trends": research_report.get("industry_trends", "No data available")
    }
    
    input_data = {
        "prospect_name": prospect_name,
        "company_name": company_name,
        "company_overview": formatted_report["company_overview"],
        "key_contacts": formatted_report["key_contacts"],
        "recent_news": formatted_report["recent_news"],
        "industry_trends": formatted_report["industry_trends"],
        "product_catalog": product_catalog
    }
    
    response = chain.invoke(input_data)
    
    return response.strip()
