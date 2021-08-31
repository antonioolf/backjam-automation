import json
import os
from functions import Functions


def update_public_list(data):
    print('Atualizando lista pública do aplicativo')
    with open('backing-tracks.json', 'w') as file:
        file.write(data)


def delete_synchronized_files(google_drive_files):
    local_to_upload_files = [
        f.replace('./to-upload/', '')
        for f in Functions.list_from_folder('to-upload', '.+\\.mp3')
    ]

    for synchronized_item in google_drive_files:
        if synchronized_item['full_name'] in local_to_upload_files:
            print(f'Deletando arquivo já sincronizado ({synchronized_item["full_name"]})')
            os.remove(f'./to-upload/{synchronized_item["full_name"]}')


def commit_push_backing_tracks_json():
    print('Publicando backing-tracks.json usando Git')
    os.system(
        'git init && '
        'git remote set-url origin git@github.com:antonioolf/backjam-automation.git && '
        'git add backing-tracks.json && '
        'git commit -m "Update backing-tracks.json" && '
        'git push -u origin main'
    )


def run():
    google_drive_files = Functions.get_google_drive_files_list()
    update_public_list(json.dumps(google_drive_files, indent=4))

    delete_synchronized_files(google_drive_files)
    commit_push_backing_tracks_json()


if __name__ == '__main__':
    run()
