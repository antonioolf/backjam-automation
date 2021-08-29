import os
import requests

from env import youtube_api_key, playlist_id
from functions import Functions

# TODO: Implementar paginação quando playlist completar 50 vídeos

youtube_api = 'https://www.googleapis.com/youtube/v3'
max_results = 50

playlist_videos_url = f'{youtube_api}/playlistItems?key={youtube_api_key}&playlistId={playlist_id}' \
                      f'&part=snippet,id&type=video&maxResults={max_results}'


def get_ids():
    res = requests.get(playlist_videos_url)
    result = []
    for video in res.json()['items']:
        video_id = video['snippet']['resourceId']['videoId']
        result.append(video_id)

    print(f'{len(result)} videos na playlist')
    return result


def update_to_download_file(video_ids_list):
    print('Atualizando to-download.txt')

    with open('to-download.txt', 'w') as file:
        for video_id in video_ids_list:
            file.write(f'https://www.youtube.com/watch?v={video_id}\n')


def find_ids_without_file(video_ids):
    """
    Encontra ids que ainda não tem um arquivo na pasta "to-upload" nem na pasta "downloads"
    """
    result = []
    for video_id in video_ids:
        existing_files_to_upload = Functions.list_from_folder('to-upload', f'{video_id} \\- .+')
        existing_files_downloads = Functions.list_from_folder('downloads', f'{video_id} \\- .+')

        if not existing_files_to_upload and not existing_files_downloads:
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
    video_ids = get_ids()
    video_id_without_file_list = find_ids_without_file(video_ids)
    update_to_download_file(video_id_without_file_list)
    if len(video_id_without_file_list) > 0:
        run_youtube_dl()
    else:
        print('Nenhum vídeo no arquivo to-download.txt')


if __name__ == '__main__':
    run()
