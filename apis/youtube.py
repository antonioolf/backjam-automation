import requests
from env import youtube_api_key


class YouTube:

    @staticmethod
    def get_video_ids_from_playlist(playlist_id):
        youtube_api = 'https://www.googleapis.com/youtube/v3'
        max_results = 50
        playlist_videos_url = f'{youtube_api}/playlistItems?key={youtube_api_key}&playlistId={playlist_id}' \
                              f'&part=snippet,id&type=video&maxResults={max_results}'

        res = requests.get(playlist_videos_url)
        result = []
        for video in res.json()['items']:
            video_id = video['snippet']['resourceId']['videoId']
            result.append(video_id)

        print(f'{len(result)} videos na playlist')
        return result
