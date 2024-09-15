from langchain_ollama.llms import OllamaLLM

# Initialize Ollama LLM
model = OllamaLLM(model="mixtral")
def review_email(email_draft, sample_emails):
    improve_prompt = f"""
    Improve the following email draft using best practices from the provided sales-winning email templates. Make sure to format the email as if you are drafting it directly. Do not add any extra content or suggestions. The email should not contain any asterisks and must start with "Dear"- prospect name. Do not include any introductory text like "here's your potential response".

    Email Draft:
    {email_draft}

    Sales Winning Email Templates:
    {sample_emails}

    Improved Email Draft:

    """

    improved_email_response = model(improve_prompt)
    improved_email = improved_email_response.strip()



    return {
        "improved_email": improved_email,
    }
