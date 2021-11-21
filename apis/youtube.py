import requests
from env import youtube_api_key


def get_ids_from_response(json):
    ids = []

    for video in json['items']:
        if video['status']['privacyStatus'] != 'public':
            continue

        video_id = video['snippet']['resourceId']['videoId']
        ids.append(video_id)

    return ids


def abort_invalid_request(res):
    if res.status_code >= 400:
        print(f'status_code: {res.status_code}')
        print(f'reason: {res.reason}')
        print(f'url: {res.url}')
        print(res.text)
        exit(0)


class YouTube:

    @staticmethod
    def get_video_ids_from_playlist(playlist_id):
        youtube_api = 'https://www.googleapis.com/youtube/v3'
        max_results = 50
        result = []
        playlist_videos_url = f'{youtube_api}/playlistItems?' \
                              f'key={youtube_api_key}' \
                              f'&playlistId={playlist_id}' \
                              f'&part=snippet,id,status' \
                              f'&type=video' \
                              f'&maxResults={max_results}'

        res = requests.get(playlist_videos_url)
        while True:
            abort_invalid_request(res)

            json = res.json()
            result += get_ids_from_response(json)

            if "nextPageToken" in json:
                next_page_token = json['nextPageToken']
                res = requests.get(f'{playlist_videos_url}&pageToken={next_page_token}')
            else:
                break

        print(f'{len(result)} videos na playlist')
        return result
