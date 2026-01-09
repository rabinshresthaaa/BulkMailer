# BulkMailer
A Python script to send bulk emails to multiple recipients efficiently.

## Features
- Send emails to multiple recipients from a list.
- Attach files to emails if desired.

## Prerequisites
- Python 3.x
- Required Python packages: `smtplib`, `email`, `json`, `os`, `time`
- A valid SMTP credentials

## SetUp
1. Clone the Repository
   ```
   git clone https://github.com/rabinshresthaaa/BulkMailer.git
   cd BulkMailer
   ```
2. Setup Configuration File
   You have to edit `email_config.json` file with your credentials. For credentials you can use gmail service.
3. Prepare Recipient List
   For this, you have to add list of receiver's email address in `emails.txt` file line by line
   For example:
   ```
   email1@domain.com
   email2@domain.com
   
   ```
4. And You are good to go :)
   ```
   python send_main.py
   ```
