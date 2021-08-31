import os
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']


class GoogleDrive:

    @staticmethod
    def google_drive_auth():
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())
        return credentials

    @staticmethod
    def get_google_drive_files_list():
        credentials = Functions.google_drive_auth()
        service = build('drive', 'v3', credentials=credentials)

        files = service.files()
        request = files.list(q="fileExtension='mp3' and trashed = false", pageSize=10, fields="*")

        result = []
        while request is not None:
            response = request.execute()
            request = files.list_next(request, response)
            items = response.get('files', [])

            if not items:
                print('Nenhum arquivo no Google Drive')
                continue

            for item in items:
                matches = re.compile('.+- duration={{\\d+}} - (.+)\\.mp3').match(item["name"])
                clean_name = matches.groups()[0]
                result.append({
                    'name': clean_name,
                    'full_name': item["name"],
                    'url': item['webContentLink']
                })

        return result
