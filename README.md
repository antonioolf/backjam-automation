# BackJam Automation

Script criado com o objetivo de automatizar o processo de adição de músicas no aplicativo [BackJam](https://play.google.com/store/apps/details?id=com.backing).

De forma geral, o processo consiste em baixar como `mp3` os vídeos de uma determinada playlist do YouTube (que é alimentada manualmente com vídeos livres de direitos autorais e royalties), subir os arquivos para uma pasta pública no Google Drive e publicar a lista de links em um arquivo `json` que será lido pelo aplicativo.

Para implementar a automação foram utilizados:
- [Google Drive API](https://developers.google.com/drive/api/v3/about-sdk) 
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [youtube-dl](https://youtube-dl.org/)
- [Mutagen](https://github.com/mutagen-io/mutagen)

A automação possui os seguintes 4 módulos: `download.py`, `upload.py`, `publish.py` e `remove.py` cujas responsabilidades são explicadas a seguir:

### Download
- Obtém a lista de ids de vídeos de uma playlista do YouTube
- Filtra os ids vindos da playlist que não estão no Google Drive nem nas pastas "downloads" e "to-upload"
- Atualiza a lista de vídeos a serem baixados (`to-download.txt`)
- Executa [youtube-dl](https://youtube-dl.org/) para baixar o áudio (`mp3`) dos vídeos presentes na lista

### Upload
- Deleta arquivos corrompidos e arquivos que não estão no formato `mp3`
- Deleta arquivos mp3 cuja a duração tenha uma diferença do vídeo original maior do que `2s` 
- Faz o upload dos arquivos que ainda não foram sincronizados no Google Drive
- Deleta arquivos locais que foram sincronizados com o Google Drive

### Publish
- Atualiza lista que será utilizada para alimentar o aplicativo (`backing-tracks.json`)
- Commita as alterações do arquivo `backing-tracks.json` e sobe para o repositório.

### Remove
- Obtém lista de vídeos da playlist do YouTube
- Obtém lista de arquivos do Google Drive, confronta com lista do YouTube e verifica se algum arquivo deve ser removido do Google Drive.
- Deleta do Google Drive os arquivos obtidos na verificação
- Obtém a lista de arquivos do Google Drive, desta vez atualizada
- Atualiza, commita e sobe arquivo backing-tracks.json atualizado

## TO-DO list
- [ ] Fazer tratativas necessárias para a automação e aplicativo quando a playlist atingir o limite de 5000 vídeos
