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
IMAP_PASSWORD = 'smtp-api-key'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# File paths for JSON storage
DB_FOLDER = 'db'
PROSPECTS_FILE = os.path.join(DB_FOLDER, 'prospects.json')
SENT_EMAILS_FILE = os.path.join(DB_FOLDER, 'sent_emails.json')
REPLIED_THREADS_FILE = os.path.join(DB_FOLDER, 'replied_threads.json')

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

def insert_sent_email(to_address, original_subject, response_body, thread_id):
    sent_emails = load_json(SENT_EMAILS_FILE)
    email_entry = {"to_address": to_address, "original_subject": original_subject, "response_body": response_body, "thread_id": thread_id}
    sent_emails[len(sent_emails) + 1] = email_entry
    save_json(SENT_EMAILS_FILE, sent_emails)

def insert_replied_thread(thread_id):
    replied_threads = load_json(REPLIED_THREADS_FILE)
    replied_threads[thread_id] = True
    save_json(REPLIED_THREADS_FILE, replied_threads)

def has_replied_thread(thread_id):
    replied_threads = load_json(REPLIED_THREADS_FILE)
    return replied_threads.get(thread_id, False)

def is_reply_to_sent_email(thread_id):
    sent_emails = load_json(SENT_EMAILS_FILE)
    for email_entry in sent_emails.values():
        if email_entry.get("thread_id") == thread_id:
            return True
    return False

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
            raw_message = mail.fetch([uid], ['BODY[]', 'FLAGS', 'INTERNALDATE'])
            raw_email = raw_message[uid][b'BODY[]']
            msg = email.message_from_bytes(raw_email)

            subject = msg.get('Subject', 'No Subject')
            from_address = email.utils.parseaddr(msg.get('From'))[1]
            message_id = msg.get('Message-ID')
            in_reply_to = msg.get('In-Reply-To')
            references = msg.get('References')

            thread_id = in_reply_to or references or message_id or str(uid)

            if has_replied_thread(thread_id) or is_reply_to_sent_email(thread_id):
                print(f"Skipping email from {from_address} as it is a reply to one of our sent emails or already replied.")
                continue  # Skip if already replied to this thread or if it's a reply to one of our emails

            if not in_reply_to and not references:
                print(f"Skipping email from {from_address} as it is not a reply.")
                continue  # Skip if it's not a reply

            body = extract_body(msg)

            response = generate_response(body)

            send_response(from_address, subject, response, thread_id)

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
    You are an AI sales assistant. Based on the following email received from a prospect, please draft a professional reply.
    Make sure to format the email as if you are drafting it directly. Do not add any extra content or suggestions. The email should not contain any asterisks and must start with "Dear"- prospect name. Do not include any introductory text like "here's your potential response"

    Email received from the prospect:
    {email_body}

    The response should acknowledge the prospect's queries, provide clear answers, and encourage the prospect to engage further. Use a friendly yet formal tone.
    """
    
    response = model(prompt)
    
    return response.strip()

# Send the response via email
def send_response(to_address, original_subject, response_body, thread_id):
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
            insert_sent_email(to_address, original_subject, response_body, thread_id)
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
