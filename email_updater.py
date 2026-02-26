import smtplib
import ssl
from email.message import EmailMessage
from market_text import get_text
from gainers_and_losers import gain_and_lose_text, indicies_text, earnings_text
from datetime import date
import os
from dotenv import load_dotenv

# keys from .env
load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")


subject = date.today().strftime("%m/%d/%Y") + " Market Update" # email subject

# email body (with console output of progress)
body = ""
print("Runnning")
body += get_text()
print("Summary Added")
body += indicies_text() 
print("Indicies Added")
body += gain_and_lose_text()
print("Gainers and Losers Added")
body += earnings_text() 
print("Earnings Added")

# email content
msg = EmailMessage()
msg.set_content(body)
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = receiver_email

# server
smtp_server = os.getenv("SMTP_SERVER")
port = int(os.getenv("SMTP_PORT", 587))
context = ssl.create_default_context()

try: # try sending
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.send_message(msg)
    print("Email sent succesfully!")
except smtplib.SMTPException as e: # failed
    print(f"Error: {e}")