import imaplib
import email
from email.header import decode_header
import time

import config

# Gmail IMAP server
IMAP_SERVER = config.IMAP_SERVER
EMAIL_ACCOUNT = config.EMAIL_ACCOUNT
EMAIL_PASSWORD = config.EMAIL_PASSWORD

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

# Select the mailbox (inbox)
mail.select("inbox")

# Search for all emails
status, messages = mail.search(None, "UNSEEN")
# status, messages = mail.search(None, "ALL")
# print(status, messages)
# isi variable `messages` = [b'1 2 9 20 203'] => '1 2 9 20 203' => [1,2,9,20,203]
# print(messages[0].decode('utf-8'))

# # Convert messages to a list of email IDs
email_ids = messages[0].decode('utf-8').split() # whitespace = ' ', '\n' ,'\t'
# print(email_ids) # eg. = [1,2,3,4,5]
# print(email_ids[-2:]) # [4,5]
# print(email_ids[len(email_ids-2):len(email_ids-1)]) # email_ids[3:4], di python index start dari 0

# Fetch the latest 2 emails
for email_id in email_ids[-2:]:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    # print(msg_data)
    # base64 
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Extract sender
            msg = email.message_from_bytes(response_part[1])
            # print(msg)
            from_email = msg.get("From")
            print(f"From: {from_email}")
#             # rahard@gmail.com -> Budi Rahardjo <rahard@gmail.com>
#             # if 'rahard@gmail.com' in from_email:
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode("utf-8")
            print(f"Subject: {subject}")

            # Extract email body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    print(content_type)
                    body = part.get_payload(decode=True)
                    print(f"Body:\n{body}\n")
                    if content_type == "text/csv":
                        body = body.decode()
                        f = open('hasil.csv', 'w')
                        f.write(body)
                        f.close()
                    elif content_type == 'image/jpg':
                        body = body.decode()
                        f = open(f'{time.time()}-image.jpg', 'w')
                        f.write(body)
                        f.close()
                    elif content_type == 'text/html':
                        body = body.decode()
                        f = open('email.html', 'w')
                        f.write(body)
                        f.close()
                    elif content_type == 'text/plain':
                        # body = body.decode()
                        f = open('plaintext.txt', 'wb')
                        f.write(body)
                        f.close()
            else:
                body = msg.get_payload(decode=True).decode()
                print(f"Body:\n{body}\n")

# Close the connection
mail.logout()