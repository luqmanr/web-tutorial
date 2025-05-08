import imaplib
import email
from email.header import decode_header

# Gmail IMAP server
IMAP_SERVER = "imap.borma.com"
EMAIL_ACCOUNT = "andre@borma.cc"
EMAIL_PASSWORD = "passwordbiasa"

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

# Select the mailbox (inbox)
mail.select("inbox")

# Search for all emails
# status, messages = mail.search(None, "UNSEEN")
status, messages = mail.search(None, "ALL")

# Convert messages to a list of email IDs
email_ids = messages[0].split()

# Fetch the latest 5 emails
for email_id in email_ids[-2:]:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Extract sender
            msg = email.message_from_bytes(response_part[1])
            from_email = msg.get("From")
            # rahard@gmail.com -> Budi Rahardjo <rahard@gmail.com>
            # if 'rahard@gmail.com' in from_email:
            print(f"From: {from_email}")
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            print(f"Subject: {subject}")

            # Extract email body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    print(content_type)
                    if content_type == "text/csv":
                        body = part.get_payload(decode=True).decode()
                        f = open('hasil.csv', 'w')
                        f.write(body)
                        f.close()
                        print(f"Body:\n{body}\n")
            else:
                body = msg.get_payload(decode=True).decode()
                print(f"Body:\n{body}\n")

# Close the connection
mail.logout()