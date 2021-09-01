import json

from apis.google_drive import GoogleDrive
from functions import Functions


def update_public_list(data):
    print('Atualizando lista pública do aplicativo')
    with open('backing-tracks.json', 'w') as file:
        file.write(data)


def run():
    google_drive_files = GoogleDrive.get_google_drive_files_list()
    update_public_list(json.dumps(google_drive_files, indent=4))

    Functions.commit_push_backing_tracks_json()


if __name__ == '__main__':
    run()
