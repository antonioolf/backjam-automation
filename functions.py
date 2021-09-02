import os
import re
from env import gh_token


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
            # f'git remote add origin https://antonioolf:{gh_token}@backjam-automation.git'
            f'git remote add set-url https://antonioolf:{gh_token}@backjam-automation.git && '
            # 'git reset && '
            'git config --global user.email "backjam.app@gmail.com" && '
            'git config --global user.name "BackJam" && '
            'git add backing-tracks.json && '
            'git commit -m "Update backing-tracks.json" && '
            f'git push https://{gh_token}@github.com/antonioolf/backjam-automation.git'
        )
