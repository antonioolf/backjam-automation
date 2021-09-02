from __future__ import print_function

import math
import os
import shutil

from googleapiclient.http import MediaFileUpload
from mutagen.mp3 import MP3

import os.path
from googleapiclient.discovery import build
import re

from apis.google_drive import GoogleDrive
from env import google_drive_public_folder_id
from functions import Functions


def is_broken(file):
    audio = MP3(file)
    duration_file = math.ceil(audio.info.length)

    p = re.compile('.+ - duration={{(\\d+)}} - .+\\.mp3')
    duration_name = int(p.match(file).groups()[0])

    difference = abs(duration_name - duration_file)

    broken = difference > 2
    msg = 'Corrompido' if broken else 'Ok'

    print(f'Diferença: {difference}s - {file[12:26]} {msg}')

    # Diferença de tempo é maior que 2 segundos?
    return broken


def upload_unlisted_files(google_drive_existent_files):
    files_in_upload_folder = Functions.list_from_folder('to-upload', '.+\\.mp3')
    if len(files_in_upload_folder) == 0:
        print('Nenhum arquivo para subir')
        return

    credentials = GoogleDrive.google_drive_auth_s_a()
    service = build('drive', 'v3', credentials=credentials)

    for local_file in files_in_upload_folder:
        clean_filename = local_file.replace('./to-upload/', '')

        if clean_filename in [file['full_name'] for file in google_drive_existent_files]:
            print(f'Arquivo já disponível no Google Drive: "{clean_filename}"')
            continue

        file_metadata = {
            'name': clean_filename,
            'parents': [google_drive_public_folder_id]
        }

        print(f'Fazendo upload... ({clean_filename})')
        media = MediaFileUpload(local_file, mimetype='audio/mpeg', resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f'Finalizado! Id: {file.get("id")} \n')


def move_to_upload_folder_or_delete_broken(files):
    print('Verificando se arquivos estão corrompidos de acordo com a diferença de tempo')
    for file in files:
        broken = is_broken(file)

        if broken:
            os.remove(file)
            print(f'Arquivo corrompido excluído: {file}')
        else:
            shutil.move(file, f'./to-upload/{file.replace("./downloads/", "")}')


def delete_synchronized_files(google_drive_files):
    local_to_upload_files = [
        f.replace('./to-upload/', '')
        for f in Functions.list_from_folder('to-upload', '.+\\.mp3')
    ]

    for synchronized_item in google_drive_files:
        if synchronized_item['full_name'] in local_to_upload_files:
            print(f'Deletando arquivo já sincronizado ({synchronized_item["full_name"]})')
            os.remove(f'./to-upload/{synchronized_item["full_name"]}')


def run():
    Functions.delete_non_mp3_files()
    files = Functions.list_from_folder('downloads', '.+\\.mp3')

    if len(files) == 0:
        print('Nenhum arquivo disponível na pasta downloads')
    else:
        move_to_upload_folder_or_delete_broken(files)

    google_drive_files = GoogleDrive.get_google_drive_files_list()
    upload_unlisted_files(google_drive_files)

    google_drive_files = GoogleDrive.get_google_drive_files_list()
    delete_synchronized_files(google_drive_files)


if __name__ == '__main__':
    run()
