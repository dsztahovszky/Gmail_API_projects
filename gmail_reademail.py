from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_messages(service):
    results = service.users().messages().list(userId='me').execute()
    msg_ids = []
    for msg in results['messages']:
        msg_ids.append(msg['id'])
    mail_data = input('Add meg angolul, vesszővel és szóközzel elválasztva, hogy leveleid mely adatát szeretnéd kiíratn'
                      'i a képernyőre (pl From)!\t')
    for index in range(int(input('Írd ide, hogy hány levél adatait szeretnéd megjeleníteni!\t'))):
        message = service.users().messages().get(userId='me',
                                                 id=msg_ids[index], format='metadata').execute()
        headers = message['payload']['headers']
        print()
        for header in headers:
            if header['name'] == mail_data:
                print(f'{index + 1}.:\n{mail_data}: {header["value"]}')


def main():
    service = get_service()
    get_messages(service)


main()
