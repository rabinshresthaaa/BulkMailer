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

#ask user if they want to attach file in email
def include_file():
    if input("Do you want to attach a file to your email? (Y/N): ").strip().lower() == 'y':
        print("You must have file in the same directory.")
        filename = input("Enter filename: ")
        while not os.path.exists(os.path.join(os.getcwd(), filename)):
            filename = input("File not not exist. Please Enter Again (with extension)\n OR \nPress Q to continue without attacking file: ")
            if filename.lower() == 'q':
                return None
        return filename
    else:
        return None

#returns list of receiver emails
def receiver_emails(files):
    with open(files, 'r') as file:
        emails = file.read().splitlines()
    return emails 

#this asks subject and message from user
def get_message():
    subject = input("Enter subject of your email: ")
    message = input("Enter message: ")
    return subject, message

# this function attaches file in email
def attach_file(msg,filename):
    with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)

## sends email
def send_mail(to_email,subject, message,filename):
    from_email = f"{sender_name} <{username}>"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, "plain"))
    #check if user wants to attach file in pdf
    if filename:
        attach_file(msg,filename)
    msg['To'] = to_email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            print("Email send successfully to", msg['To'],"!!")
    except Exception as e:
        print("Failed to send email to",msg['To'],f"\nError Occured: {e}!!")

def main():
    emails = receiver_emails("emails.txt")
    if emails == []:
        print("No Email in List")
        return ""
    subject, message = get_message()
    filename = include_file()
    for email in emails:
        send_mail(email,subject, message,filename)
        time.sleep(3)
    print("Task Completed!")


if __name__ == '__main__':
    main()