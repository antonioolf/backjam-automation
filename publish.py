import sys

import json

from apis.google_drive import GoogleDrive
from functions import Functions


def update_public_list(data, playlist_id):
    print(f'Atualizando lista pública "{playlist_id}"')
    with open(f'json/playlists/{playlist_id}.json', 'w') as file:
        file.write(data)


def run(playlist_id):
    google_drive_files = GoogleDrive.get_google_drive_files_list()
    update_public_list(json.dumps(google_drive_files, indent=4), playlist_id)

    Functions.commit_push_backing_tracks_json()


if __name__ == '__main__':
    playlist_id_argument = sys.argv[1:]
    if playlist_id_argument is not None:
        run(playlist_id_argument)
