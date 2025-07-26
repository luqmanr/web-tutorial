import imaplib
import email
from email.header import decode_header
import time

import config
import sendmail
import readdatabase

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
# status, messages = mail.search(None, "UNSEEN")
status, messages = mail.search(None, "ALL")

# # Convert messages to a list of email IDs
email_ids = messages[0].decode('utf-8').split()

# Fetch the latest 2 emails
for email_id in email_ids[-10:]:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    # base64 
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Extract sender
            msg = email.message_from_bytes(response_part[1])
            from_email = msg.get("From")
            # STEPS to sanitize
            # 1. "Luqman Rahard ID <luqmanr.rahardjo@gmail.com>"
            # 2. ["Luqman Rahard ID", "luqmanr.rahardjo@gmail.com>"]
            # 3. ambil index terakhir [-1] -> "luqmanr.rahardjo@gmail.com>"
            # 4. replace(">", "") -> "luqmanr.rahardjo@gmail.com"
            from_email = from_email.split("<")
            from_email = from_email[-1]
            from_email = from_email.replace(">", "")
            print(from_email)
            # rayner@gmail.com
            # rayner.1234@gmail.com
            # 1234rayner@gmail.com
            if 'no-reply@lalamove.com' == from_email:
                print(f"From: {from_email}")
    #             # rahard@gmail.com -> Budi Rahardjo <rahard@gmail.com>
    #             # if 'rahard@gmail.com' in from_email:
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode("utf-8")
                print(f"Subject: {subject}")

                # cari rekno & jumlah dari database
                rekno, jumlah = readdatabase.get_rekno_jumlah('luqman.rahardjo@gmail.com')
                # hit LLM API
                # email_msg = LLM(from_email, rekno, jumlah)
                # email_msg = """
                #   Selamat siang {from_email} dengan norek: {rekno}
                #   anda sudah memiliki {jumlah} di rekening anda
                #   wah angkanya sudah sangat besar, dsb... dsb...
                # """

                reply_subject = 'rekno & jumlah anda'
                reply_body = f"""
                    rekno: {rekno}
                    jumlah: {jumlah}
                    """
                sendmail.send_gmail_email(
                    EMAIL_ACCOUNT,
                    EMAIL_PASSWORD,
                    'luqman.rahardjo@gmail.com', 
                    reply_subject,
                    reply_body)

