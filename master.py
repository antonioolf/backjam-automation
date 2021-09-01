import download
import publish
import remove
import upload
from env import google_drive_public_folder_id, playlist_id

if __name__ == '__main__':
    print(f'>>>>>>>>>> {google_drive_public_folder_id}')
    print(f'>>>>>>>>>> {playlist_id}')

    exit(0)

    download.run()
    upload.run()
    publish.run()
    remove.run()
