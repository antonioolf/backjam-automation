import os
import re


class Functions:

    @staticmethod
    def list_from_folder(folder, pattern):
        raw_list = os.listdir(f'./{folder}')
        p = re.compile(pattern)
        return [f'./{folder}/{s}' for s in raw_list if p.match(s)]

    @staticmethod
    def delete_non_mp3_files():
        non_mp3_files = Functions.list_from_folder('downloads', '^(?!.*?.+\\.mp3).*')
        for file in non_mp3_files:
            if '/.gitkeep' in file:
                continue
            os.remove(file)

    @staticmethod
    def commit_push_backing_tracks_json():
        print('Publicando backing-tracks.json usando Git')
        os.system(
            'git init && '
            'git remote set-url origin git@github.com:antonioolf/backjam-automation.git && '
            'git reset && '
            'git add backing-tracks.json && '
            'git commit -m "Update backing-tracks.json" && '
            'git push -u origin main'
        )
