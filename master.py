import json

import download
import publish
import remove
import upload


def get_playlists_objs():
    with open('json/playlists-index.json') as f:
        ids = json.load(f)
        return ids


if __name__ == '__main__':
    playlist_objs = get_playlists_objs()

    for obj in playlist_objs:
        download.run(obj['playlist_id'])
        upload.run()
        publish.run(obj['playlist_id'])
        remove.run(obj['playlist_id'])
