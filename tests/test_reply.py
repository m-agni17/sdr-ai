import imapclient
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_ollama.llms import OllamaLLM
import schedule
import time
from threading import Thread
import json
import os

IMAP_SERVER = 'imap.gmail.com'
IMAP_USER = 'salesrepresent124@gmail.com'
IMAP_PASSWORD = 'ochp ckfu llyd lwqa'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# File paths for JSON storage
PROSPECTS_FILE = 'prospects.json'
SENT_EMAILS_FILE = 'sent_emails.json'
REPLIED_THREADS_FILE = 'replied_threads.json'

# Initialize LLM model
model = OllamaLLM(model="llama3.1")

# Helper functions for JSON storage
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Create initial empty JSON files if they don't exist
def initialize_json_files():
    if not os.path.exists(PROSPECTS_FILE):
        save_json(PROSPECTS_FILE, {})
    if not os.path.exists(SENT_EMAILS_FILE):
        save_json(SENT_EMAILS_FILE, {})
    if not os.path.exists(REPLIED_THREADS_FILE):
        save_json(REPLIED_THREADS_FILE, {})

def insert_prospect(name, company, additional_info=''):
    prospects = load_json(PROSPECTS_FILE)
    prospects[name] = {"company": company, "additional_info": additional_info}
    save_json(PROSPECTS_FILE, prospects)

def insert_sent_email(to_address, original_subject, response_body):
    sent_emails = load_json(SENT_EMAILS_FILE)
    email_entry = {"to_address": to_address, "original_subject": original_subject, "response_body": response_body}
    sent_emails[len(sent_emails) + 1] = email_entry
    save_json(SENT_EMAILS_FILE, sent_emails)

def insert_replied_thread(thread_id):
    replied_threads = load_json(REPLIED_THREADS_FILE)
    replied_threads[thread_id] = True
    save_json(REPLIED_THREADS_FILE, replied_threads)

def has_replied_thread(thread_id):
    replied_threads = load_json(REPLIED_THREADS_FILE)
    return replied_threads.get(thread_id, False)

# Check for replies in the inbox
def check_for_replies():
    try:
        mail = imapclient.IMAPClient(IMAP_SERVER, ssl=True)
        mail.login(IMAP_USER, IMAP_PASSWORD)
        mail.select_folder('INBOX', readonly=True)

        uids = mail.search(['UNSEEN'])
        
        if not uids:
            print("No new emails.")
            return
        
        for uid in uids:
            raw_message = mail.fetch([uid], ['BODY[]', 'FLAGS'])
            raw_email = raw_message[uid][b'BODY[]']
            msg = email.message_from_bytes(raw_email)

            subject = msg.get('Subject', 'No Subject')
            from_address = email.utils.parseaddr(msg.get('From'))[1]
            thread_id = msg.get('In-Reply-To') or msg.get('References') or str(uid)

            if has_replied_thread(thread_id):
                print(f"Already replied to thread: {thread_id}")
                continue  # Skip if already replied to this thread

            body = extract_body(msg)

            response = generate_response(body)

            send_response(from_address, subject, response)

            insert_replied_thread(thread_id)

        print("Email check and response sent.")

    except Exception as e:
        print(f"Error checking emails: {str(e)}")

# Extract body from email
def extract_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')
    else:
        return msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')

    return "No text part found."

# Generate a response using the model
def generate_response(email_body):
    prompt = f"""
    The following is an email received from a prospect:

    Email Body:
    {email_body}

    Based on the context of the email, generate a professional and appropriate response.
    """
    
    response = model(prompt)
    
    return response.strip()

# Send the response via email
def send_response(to_address, original_subject, response_body):
    msg = MIMEMultipart()
    msg['From'] = IMAP_USER
    msg['To'] = to_address
    msg['Subject'] = f"Re: {original_subject}"

    msg.attach(MIMEText(response_body, 'plain'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(IMAP_USER, IMAP_PASSWORD)
            server.sendmail(IMAP_USER, to_address, msg.as_string())
            print(f"Response sent to {to_address}")
            insert_sent_email(to_address, original_subject, response_body)
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Email checking loop
def email_check_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every(60).seconds.do(check_for_replies)

if __name__ == "__main__":
    initialize_json_files()
    email_thread = Thread(target=email_check_loop)
    email_thread.start()

    print("Email checking service started.")
