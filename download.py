import os
import re

from apis.youtube import YouTube
from env import playlist_id
from functions import Functions
from apis.google_drive import GoogleDrive


def update_to_download_file(video_ids_list):
    print('Atualizando to-download.txt')

    with open('to-download.txt', 'w') as file:
        for video_id in video_ids_list:
            file.write(f'https://www.youtube.com/watch?v={video_id}\n')


def find_ids_without_file(video_ids):
    """
    Encontra ids que ainda não tem um arquivo no Google Drive nem na pasta "to-upload" e nem na pasta "downloads"
    """
    result = []
    google_drive_files = [file['full_name'] for file in GoogleDrive.get_google_drive_files_list()]
    print(f'{len(google_drive_files)} arquivos no Google Drive')

    for video_id in video_ids:
        existing_files_to_upload = Functions.list_from_folder('to-upload', f'{video_id} \\- .+')
        existing_files_downloads = Functions.list_from_folder('downloads', f'{video_id} \\- .+')

        p = re.compile(f'{video_id} - .+')
        existing_files_google_drive = [g for g in google_drive_files if p.match(g)]

        if len(existing_files_to_upload) == 0 and \
                len(existing_files_downloads) == 0 and \
                len(existing_files_google_drive) == 0:
            result.append(video_id)

    print(f'{len(result)} videos sem mp3 baixado')
    return result


def run_youtube_dl():
    print('Executando youtube-dl...')
    os.system('youtube-dl --extract-audio --audio-format mp3 '
              '-o "./downloads/%(id)s - duration={{%(duration)s}} - %(title)s.%(ext)s" '
              '--batch-file=./to-download.txt')


def run():
    Functions.delete_non_mp3_files()
    video_ids = YouTube.get_video_ids_from_playlist(playlist_id)
    video_id_without_file_list = find_ids_without_file(video_ids)
    update_to_download_file(video_id_without_file_list)
    if len(video_id_without_file_list) > 0:
        run_youtube_dl()
    else:
        print('Nenhum vídeo no arquivo to-download.txt')


if __name__ == '__main__':
    run()
