import streamlit as st
import requests

FASTAPI_BASE_URL = "http://localhost:8000"

if 'research_report' not in st.session_state:
    st.session_state.research_report = None
if 'product_catalog' not in st.session_state:
    st.session_state.product_catalog = None
if 'email_draft' not in st.session_state:
    st.session_state.email_draft = None
if 'sample_emails' not in st.session_state:
    st.session_state.sample_emails = None
if 'improved_email' not in st.session_state:
    st.session_state.improved_email = None

st.title("Prospect Email Automation System")

# Step 1: Generate Research Report
with st.form(key='research_form'):
    st.header("1. Generate Research Report")
    col1, col2 = st.columns(2)
    with col1:
        prospect_name = st.text_input("Prospect Name")
    with col2:
        company_name = st.text_input("Company Name")
    additional_info = st.text_area("Additional Information (optional)")
    
    submit_button = st.form_submit_button("Generate Research Report")

    if submit_button:
        if not prospect_name or not company_name:
            st.error("Please enter both Prospect Name and Company Name.")
        else:
            try:
                response = requests.post(f"{FASTAPI_BASE_URL}/research", json={
                    "prospect_name": prospect_name,
                    "company_name": company_name,
                    "additional_info": additional_info
                })
                response.raise_for_status()

                data = response.json()
                research_report = data.get("research_report", {})
                st.write("### CrewAI Research Report")
                if research_report:
                    st.write(research_report)
                    st.session_state.research_report = research_report
                else:
                    st.write("No CrewAI research report found.")
            except requests.RequestException as e:
                st.error(f"Failed to generate research report: {e}")

# Step 2: Upload Product Catalog and Generate Personalized Email
if st.session_state.research_report:
    st.write("Research Report:")
    st.text_area('Research Report', st.session_state.research_report, height=300)

    st.header("2. Upload Product Catalog")
    product_catalog_file = st.file_uploader('Upload Product Catalog (TXT file)', type='txt')
    
    if product_catalog_file is not None:
        st.session_state.product_catalog = product_catalog_file.read().decode("utf-8")
        st.write('Product Catalog uploaded successfully!')

        if st.button('Generate Personalized Email'):
            with st.spinner('Generating email...'):
                try:
                    email_response = requests.post(f"{FASTAPI_BASE_URL}/generate_email", json={
                        "prospect_name": prospect_name,
                        "company_name": company_name,
                        "research_report": st.session_state.research_report,
                        "product_catalog": st.session_state.product_catalog
                    })
                    email_response.raise_for_status()
                    st.session_state.email_draft = email_response.json().get("email_draft", "")
                    st.write("Generated Email Draft:")
                    st.text_area('Email Draft', st.session_state.email_draft, height=300)
                except requests.RequestException as e:
                    st.error(f"Failed to generate email: {e}")

# Step 3: Upload Sales Email Templates
if st.session_state.email_draft:
    st.header("3. Upload Sales Email Templates")
    sample_emails_file = st.file_uploader('Upload Sales Email Templates (TXT file)', type='txt')

    if sample_emails_file is not None:
        st.session_state.sample_emails = sample_emails_file.read().decode("utf-8")
        st.write('Sales Email Templates uploaded successfully!')

        if st.button('Review and Improve Email'):
            with st.spinner('Reviewing email...'):
                try:
                    review_response = requests.post(f"{FASTAPI_BASE_URL}/review_email", json={
                        "email_draft": st.session_state.email_draft,
                        "sample_emails": st.session_state.sample_emails
                    })
                    review_response.raise_for_status()
                    improved_result = review_response.json()
                    st.session_state.improved_email = improved_result['improved_email']
                    st.write("Reviewed and Improved Email Draft:")
                    st.text_area('Improved Email Draft', st.session_state.improved_email, height=300)
                except requests.RequestException as e:
                    st.error(f"Failed to review email: {e}")

# Step 4: Send Email
if st.session_state.improved_email:
    st.header("4. Send Email")
    sender_email = st.text_input('Sender Email')
    recipient_email = st.text_input('Recipient Email')
    subject = st.text_input('Email Subject')

    if st.button('Send Email'):
        if sender_email and recipient_email and subject:
            try:
                email_response = requests.post(f"{FASTAPI_BASE_URL}/send_email", json={
                    "sender_email": sender_email,
                    "recipient_email": recipient_email,
                    "subject": subject,
                    "email_body": st.session_state.improved_email
                })
                email_response.raise_for_status()
                st.success("Email sent successfully!")
            except requests.RequestException as e:
                st.error(f"Failed to send email: {e}")
        else:
            st.error("Please provide all required fields: Sender Email, Recipient Email, and Subject.")
