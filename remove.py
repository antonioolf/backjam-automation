import sys

import json
import re

from apis.google_drive import GoogleDrive
from apis.youtube import YouTube
from functions import Functions


def get_to_remove_list(playlist_id):
    playlist_video_ids = YouTube.get_video_ids_from_playlist(playlist_id)
    google_drive_files = GoogleDrive.get_google_drive_files_list()

    to_remove = []

    for drive_file in google_drive_files:
        matches = re.compile('(.+) - duration={{\\d+}} - ').match(drive_file['full_name'])
        drive_youtube_id = matches.groups()[0]

        if drive_youtube_id not in playlist_video_ids:
            to_remove.append(drive_file)

    return to_remove


def run(playlist_id):
    to_remove_list = get_to_remove_list(playlist_id)

    if not to_remove_list:
        print("Nenhum arquivo para ser removido do Google Drive")
        return

    for file in to_remove_list:
        GoogleDrive.delete_file(file)

    google_drive_files = GoogleDrive.get_google_drive_files_list()
    print('Atualizando lista pública do aplicativo')

    with open(f'json/playlists/{playlist_id}.json', 'w') as file:
        file.write(json.dumps(google_drive_files, indent=4))

    Functions.commit_push_backing_tracks_json()


if __name__ == '__main__':
    playlist_id_argument = sys.argv[1:]
    if playlist_id_argument is not None:
        run(playlist_id_argument)
