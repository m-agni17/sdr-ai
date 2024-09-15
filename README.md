markdown
Copy code
# AI-Powered SDR Email Outreach System

## Overview

This project is an AI-powered Sales Development Representative (SDR) Email Outreach System designed to streamline the email outreach process for sales teams. The system automates key tasks such as prospect research, email generation, review, and sending, ensuring personalized and effective communication with prospects.

## Features

- **Prospect Research**: Automates the gathering of information about prospects and their companies.
- **Email Generation**: Creates personalized email drafts based on prospect data and product catalog.
- **Email Review**: Refines email drafts by comparing them to winning sales email templates.
- **Email Sending**: Sends the final email to prospects using SMTP integration.
- **Reply Handling**: Monitors and responds to incoming emails using IMAP.
- **Secure Data Handling**: Ensures data security and compliance with encryption and authentication measures.

## Technologies Used

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI Models**: LLaMA 3.1 (for email generation and research)
- **APIs**: CrewAI, Serper API
- **Email Sending**: SMTP
- **Email Reply Handling**: IMAP

## Installation

1. **Clone the Repository**

   ```
   git clone https://github.com/yourusername/sdr-email-outreach-system.git
   cd sdr-email-outreach-system
   ```
   
Set Up a Virtual Environment

```
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate'
```

Install Dependencies

pip install -r requirements.txt

Configuration

Backend Configuration: Update config.yaml with your API keys, email settings, and other configurations.
Email Sending: Set up an app-specific password for SMTP in your email account.
Usage
Start the Backend Server

```
uvicorn app:app --reload
```

Run the Frontend
```
streamlit run frontend.py
```

Interact with the System

Open your browser and navigate to http://localhost:8501 to access the Streamlit UI.
Enter prospect details and upload necessary files.
The system will handle research, email generation, review, and sending.

Contributing
Feel free to contribute to this project by submitting issues or pull requests. For significant changes, please open an issue to discuss the proposed modifications.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any questions or further information, please contact agniprasanth1723@gmail.com.



