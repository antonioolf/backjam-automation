"""
Varre pasta downloads
Verifica se o arquivo não está quebrado
Move para pasta to-upload
Pasta to-upload está sincronizada com Google Drive
"""
import os
import re
import shutil
import math
from mutagen.mp3 import MP3

from functions import Functions


def id_range_str(file):
    return file[12:26]


def without_downloads_range_str(file):
    return file[12:]


def is_broken(file):
    audio = MP3(file)
    duration_file = math.ceil(audio.info.length)

    p = re.compile('.+ - duration={{(\\d+)}} - .+\\.mp3')
    duration_name = int(p.match(file).groups()[0])

    difference = abs(duration_name - duration_file)

    broken = difference > 2
    msg = 'Corrompido' if broken else 'Ok'

    print(f'Diferença: {difference}s - {id_range_str(file)} {msg}')

    # Diferença de tempo é maior que 2 segundos?
    return broken


def run():
    Functions.delete_non_mp3_files()
    files = Functions.list_from_folder('downloads', '.+\\.mp3')

    if len(files) == 0:
        print('Nenhum arquivo disponível na pasta downloads')
    else:
        print('Verificando se arquivos estão corrompidos de acordo com a diferença de tempo')
        for file in files:
            broken = is_broken(file)

            if broken:
                os.remove(file)
                print(f'Arquivo corrompido excluído: {file}')
            else:
                shutil.move(file, f'./to-upload/{without_downloads_range_str(file)}')


if __name__ == '__main__':
    run()
