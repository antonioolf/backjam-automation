import json
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account

from env import google_drive_credentials_json

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.file'
]


class GoogleDrive:

    @staticmethod
    def google_drive_auth_s_a():
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(google_drive_credentials_json, strict=False),
            scopes=SCOPES
        )

        return credentials

    @staticmethod
    def get_google_drive_files_list():
        credentials = GoogleDrive.google_drive_auth_s_a()
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

    @staticmethod
    def delete_file(file):
        print(f'Deletando do Google Drive "{file["full_name"]}"')
        credentials = GoogleDrive.google_drive_auth_s_a()
        service = build('drive', 'v3', credentials=credentials)

        matches = re.compile('https://drive\\.google\\.com/uc\\?id=(.+)&export=download').match(file['url'])
        google_drive_id = matches.groups()[0]

        try:
            service.files().delete(fileId=google_drive_id).execute()
        except Exception as ex:
            print(ex.error_details)

    """
    # Deprecated
    @staticmethod
    def google_drive_auth_normal_user():
        credentials = None
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                credentials = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())
        return credentials
        """
