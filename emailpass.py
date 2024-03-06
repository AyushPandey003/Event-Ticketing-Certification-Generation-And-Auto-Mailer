import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os

import base64
import os
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import mimetypes
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

body='''
<html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.5;
            }
            .ticket {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                padding: 20px;
                margin-bottom: 20px;
            }
            .ticket h2 {
                color: #333;
                font-size: 24px;
                margin-bottom: 10px;
            }
            .ticket p {
                color: #666;
                font-size: 16px;
                margin-bottom: 10px;
            }
            .ticket b {
                color: #333;
            }
            .ticket .note {
                color: #999;
                font-size: 14px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="ticket">
            <h2>Event Ticket</h2>
            <p>Dear Participant,</p>
            <p>We are pleased to invite you to the upcoming event organized by Linpack Club. Attached to this email is your event ticket.</p>
            <p>Please present this ticket at the registration desk on the day of the event.</p>
            <p>We look forward to seeing you there!</p>
            <p><b>This is the final event ticket.</b></p>
            <p class="note">P.S. - If you have received previous emails regarding our event in Advitya, please ignore them as they were sent by mistake. We apologize for the inconvenience.</p>
            <p>Best regards,</p>
            <p>Linpack Club</p>
        </div>
    </body>
</html>
'''

def gmail_send_message(to, reg):
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = get_credentials()

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.add_alternative(body, subtype="html")

    message["To"] = to
    message["From"] = "Linpack Club <"your club gmail">"
    message["Subject"] = "Linpack Club Event Ticket"
    
    attachment_filename = f"certificates/{reg}_certificate.png"
    type_subtype, _ = mimetypes.guess_type(attachment_filename)
    maintype, subtype = type_subtype.split("/")

    with open(attachment_filename, "rb") as fp:
        attachment_data = fp.read()
    message.add_attachment(attachment_data, maintype, subtype, filename=f"{reg}_ticket.png")

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


data = pd.read_csv("data.csv")
emails = data.to_dict()["Email Address"]
regno = data.to_dict()["Registration Number of Member 1 (if in team)"]

emailids = {}

for key in emails.keys():
    emailids[regno[key]] = emails[key]

for key in emailids:
    gmail_send_message(emailids.get(key), key)
    print(emailids.get(key), key)






