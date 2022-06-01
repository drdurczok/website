from smtplib import SMTP_SSL, SMTP_SSL_PORT
import imaplib
import email
import traceback
import time

SMTP_HOST = 'smtp.gmail.com'
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

USER = 'reception.eac.stellar@gmail.com'
PASS = 'dysmrhmqccdsiikr'

def send_email_to_gmail():
    from_email = 'Customer Form'
    to_emails = ['reception.eac.stellar@gmail.com']
    body = "Hello, world!"
    headers = f"From: {from_email}\r\n"
    headers += f"To: {', '.join(to_emails)}\r\n"
    headers += f"Subject: Hello\r\n"
    email_message = headers + "\r\n" + body  # Blank line needed between headers and body

    # Connect, authenticate, and send mail
    smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
    smtp_server.set_debuglevel(1)  # Show SMTP server interactions
    smtp_server.login(USER, PASS)
    smtp_server.sendmail(from_email, to_emails, email_message)

    # Disconnect
    smtp_server.quit()


def read_email_from_gmail(last_email_date):
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(USER,PASS)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        latest_email_id = int(id_list[-1])

        data = mail.fetch(str(latest_email_id), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'utf-8'))
                date = msg['date']
                if date != last_email_date:
                    email_subject = msg['subject']
                    if email_subject == "A new visistor is coming":
                        msg = email.message_from_string(str(arr[1],'utf-8'))
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                msg_str = part.as_string().split("\n")
                                first_name = msg_str[3]
                                last_name = msg_str[4]
                                email_usr = msg_str[5]
                                company = msg_str[6]
                                access = 0
                                if company in "Assa Abloy":
                                    access = 1
                                else:
                                    access = 2
                                validitystart = msg_str[7]
                                validityend = msg_str[8]
                                comment = msg_str[9]
                                generate_reception_email(first_name, last_name, company, access, email_usr, comment)

                        return date
                    else:
                        print("Subject not found: " + email_subject)

    except Exception as e:
        traceback.print_exc()
        print(str(e))


def generate_reception_email(first_name, last_name, company, access, email_usr, comment):
    from_email = 'reception.eac.stellar@gmail.com'
    to_emails = ['reception.eac.stellar@gmail.com']

    link = "https://drdurczok.github.io/website/reception.html?name=" + first_name + "&access=" + access.__str__() + "&email=" + email_usr

    body = "Hello, \n\n" + first_name + " " + last_name + " from " + company + " is requesting access. \n\n" \
        + "Explanation provided by user is: \n\n" + comment + "\n\n" \
        + "Please click the following link to provide access. \n\n" + link

    headers = f"From: {from_email}\r\n"
    headers += f"To: {', '.join(to_emails)}\r\n"
    headers += f"Subject: A new visitor has sent a request\r\n"
    email_message = headers + "\r\n" + body  # Blank line needed between headers and body

    # Connect, authenticate, and send mail
    smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
    smtp_server.set_debuglevel(1)  # Show SMTP server interactions
    smtp_server.login(USER, PASS)
    smtp_server.sendmail(from_email, to_emails, email_message)

    # Disconnect
    smtp_server.quit()


last_email_date = '0'
while True:
    last_email_date = read_email_from_gmail(last_email_date)
    time.sleep(5)
