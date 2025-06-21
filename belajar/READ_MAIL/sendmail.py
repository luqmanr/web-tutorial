# https://pastebin.com/B9LyLDkQ

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config

# Your Gmail credentials
SENDER_EMAIL = "luqman.rahardjo@gmail.com"  # Replace with your Gmail address
SENDER_PASSWORD = config.APP_PASSWORD  # Replace with your App Password or Gmail password

# Recipient details
RECEIVER_EMAIL = open('penerima.txt', 'r').read().split() # Replace with the recipient's email address
# RECEIVER_EMAIL = ['luqman.rahardjo@gmail.com']
SUBJECT = "Test Email from Python"
BODY = "Hello from Python! This is a test email sent using smtplib."

def send_gmail_email(sender_email, sender_password, receiver_email, subject, body):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        # For Gmail, the SMTP server is smtp.gmail.com and the port is 587 (TLS) or 465 (SSL)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")

    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication Error: {e}")
        print("Please check your email address and password (or App Password).")
        print("If you're using a regular password, ensure 'Less secure app access' is enabled for your Google account.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    for receiver in RECEIVER_EMAIL:
        if receiver == 'andre@gmail.com':
            BODY = 'Halo'
        elif receiver == 'luqman':
            BODY = 'hei'
        send_gmail_email(SENDER_EMAIL, SENDER_PASSWORD, receiver, SUBJECT, BODY)