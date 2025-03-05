from yt_dlp import YoutubeDL
import os
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def get_download_path():
    """Cria a pasta de downloads se não existir e retorna o caminho."""
    user_home = os.path.expanduser("~")
    download_path = os.path.join(user_home, "videos baixados")
    os.makedirs(download_path, exist_ok=True)
    return download_path

def sanitize_filename(filename):
    """Remove caracteres especiais do nome do arquivo."""
    return re.sub(r'[^\w\s-]', ' ', filename).strip()

def remove_index_from_url(url):
    """Remove o parâmetro index da URL da playlist."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params.pop('index', None)  
    parsed_url = parsed_url._replace(query=urlencode(query_params, doseq=True))
    print("🔗 URL sem o parâmetro index:", urlunparse(parsed_url))
    return urlunparse(parsed_url)

def baixar_video_ou_playlist(url, path='./'):
    """Verifica se a URL é de um vídeo ou de uma playlist e baixa de acordo."""
    url = remove_index_from_url(url)  

    if 'list=' in url:
        print("🎵 Playlist detectada! Baixando todos os vídeos desde o primeiro...")
        ydl_opts = {
            'outtmpl': f'{path}/%(playlist_index)s - %(title)s.%(ext)s',  
            'format': 'bestaudio+bestevideo/best',   
            'restrictfilenames': True,               
            'ignoreerrors': True,                    
            'playliststart': 1,                      
            'merge_output_format': 'mp4',            
        }
    else:
        print("🎬 Vídeo detectado! Baixando apenas o vídeo...")
        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',  
            'format': 'bestaudio+bestevideo/best',
            'restrictfilenames': True,
            'noplaylist': True,  
            'ignoreerrors': True,
        }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("✅ Download concluído!")
        except Exception as e:
            print("❌ Erro ao baixar:", e)

def main():
    url = input("🎥 Insira a URL do vídeo ou playlist do YouTube: ")
    download_path = get_download_path()
    baixar_video_ou_playlist(url, download_path)

if __name__ == "__main__":
    main()
