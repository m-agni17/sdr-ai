from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email_generation import generate_email
from email_review import review_email
from email_sender import send_email
from threading import Thread
from email_reply import check_for_replies, email_check_loop
from research import perform_research

app = FastAPI()

class ResearchRequest(BaseModel):
    prospect_name: str
    company_name: str
    additional_info: str

class EmailGenerationRequest(BaseModel):
    prospect_name: str
    company_name: str
    research_report: dict
    product_catalog: str

class EmailReviewRequest(BaseModel):
    email_draft: str
    sample_emails: str

class EmailSendingRequest(BaseModel):
    sender_email: str
    recipient_email: str
    subject: str
    email_body: str

@app.post("/research")
async def research(request: ResearchRequest):
    try:
        research_report = perform_research(request.prospect_name, request.company_name)
        if isinstance(research_report, dict):
            return {"research_report": research_report}
        else:
            raise HTTPException(status_code=500, detail="Unexpected format in research report")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing research: {str(e)}")

# Email generation endpoint
@app.post("/generate_email")
async def generate_personalized_email(request: EmailGenerationRequest):
    try:
        email_draft = generate_email(
            request.prospect_name,
            request.company_name,
            request.research_report,
            request.product_catalog
        )
        return {"email_draft": email_draft}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating email: {str(e)}")

# Email review endpoint
@app.post("/review_email")
async def review_personalized_email(request: EmailReviewRequest):
    try:
        review_result = review_email(request.email_draft, request.sample_emails)
        return review_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reviewing email: {str(e)}")

# Email sending endpoint
@app.post("/send_email")
async def send_personalized_email(request: EmailSendingRequest):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_user = "salesrepresent124@gmail.com"
        smtp_password = "ochp ckfu llyd lwqa"  # Update with the correct credentials

        result = send_email(
            request.sender_email,
            request.recipient_email,
            request.subject,
            request.email_body,
            smtp_server,
            smtp_port,
            smtp_user,
            smtp_password
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

def start_email_monitoring():
    print("Starting email monitoring in the background...")
    email_check_loop()  
    
@app.on_event("startup")
async def startup_event():
    thread = Thread(target=start_email_monitoring, daemon=True)
    thread.start()
