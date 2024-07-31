import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import json
import os

with open("email_config.json", "r") as file:
    config = json.load(file)

sender_name = config['name']
smtp_server = config['smtp_server']
smtp_port = config['smtp_port']
username = config['username']
password = config['password']

## email format configuration
def configure_emails_and_send(email):
    from_email = f"{sender_name} <{username}>"
    to_email = email
    full_msg = get_message()
    subject = full_msg[0]
    message = full_msg[1]

    ## assign message with MIMEMultipart type
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, "plain"))
    if include_file():
        attach_file(msg)
    send_mail(msg)

#ask user if they want to attach file in email
def include_file():
    return input("Do you want to attach a file to your email? (Y/N): ").strip().lower() == 'y'

#returns list of receiver emails
def receiver_emails(files):
    with open(files, 'r') as file:
        emails = file.read().splitlines()
    return emails 

#this asks subject and message from user
def get_message():
    full_msg = []
    subject = input("Enter subject of your email: ")
    message = input("Enter message: ")
    full_msg.append(subject)
    full_msg.append(message)
    return full_msg

# this function attaches file in email
def attach_file(msg):
    print("You must have file in the same directory.")
    filename = input("Enter filename: ")
    while not os.path.exists(os.path.join(os.getcwd(), filename)):
        filename = input("File not not exist. Please Enter Again (with extension)\n OR \nPress Q to continue without attacking file: ")
        if filename.lower() == 'q':
            return
    with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)



## sends email
def send_mail(msg):
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            print("Email send successfully to", msg['To'],"!!")
    except Exception as e:
        print("Failed to send email to",msg['To'],f"\nError Occured: {e}")

def main():
    emails = receiver_emails("emails.txt")
    if emails == []:
        print("No Email in List")
        return ""
    for email in emails:
        configure_emails_and_send(email)
        time.sleep(3)
    print("Task Completed!")


if __name__ == '__main__':
    main()