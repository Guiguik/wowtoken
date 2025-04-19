import os.path
import time
from datetime import datetime
import base64
from email.message import EmailMessage
from requesttoken import get_wow_token_price
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
PRIX = 350000
SCOPES = ["https://mail.google.com/"]
previous = 0
import requests
webhook_url = "https://discord.com/api/webhooks/1362784784920870912/g-vk6LEjgRBmv4C07riWZao6xxakU51wRfyZqBrmX5yKNRVvMW-rcr09vKoLPRS5CSmW"


def send_discord_notification(webhook_url: str, message: str):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("✅ Notification Discord envoyée !")
    else:
        print(f"❌ Erreur Discord : {response.status_code} - {response.text}")


def gmail_send_message():
  """Create and insert a draft email.
   Print the returned draft's message and id.
   Returns: Draft object, including draft id and message meta data.

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  prix_eu = get_wow_token_price("eu")
  prix_eu = prix_eu.replace(" ", "")
  prix = int(prix_eu)
  print(f"[{now}] Prix du token : {prix} Gold")
  if prix < PRIX :
    return prix
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # create gmail api client
    service = build("gmail", "v1", credentials=creds)

    message = EmailMessage()
    msg = "Wow Token price : "+prix_eu
    message.set_content(msg)

    message["To"] = "guiguik17@gmail.com"
    message["From"] = "gduser2@workspacesamples.dev"
    message["Subject"] = "Wow token price"

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

  return prix


if __name__ == "__main__":
  while True:
    prix = gmail_send_message()
    if prix >= previous :
        emoji = "🟢⬆️"
    else:
        emoji = "🔴⬇️"
    m = f"🪙 Le token EU est à **{prix} Gold** {emoji}"
    if prix > PRIX:
        m = f"@everyone Prix du token WoW EU : 🪙🪙**{prix} Gold**🪙🪙"
    print(m)
    previous = prix
    send_discord_notification(webhook_url, m)
    time.sleep(600)