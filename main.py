from yt_dlp import YoutubeDL
import os
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def get_download_path():
    """Cria a pasta de downloads se não existir e retorna o caminho."""
    user_home = os.path.expanduser("~")
    download_path = os.path.join(user_home, "vídeos baixados")
    os.makedirs(download_path, exist_ok=True)
    return download_path

def sanitize_filename(filename):
    """Remove caracteres especiais do nome da pasta."""
    return re.sub(r'[^\w\s-]', ' ', filename).strip()

def remove_index_from_url(url):
    """Remove o parâmetro index da URL da playlist."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params.pop('index', None)  
    parsed_url = parsed_url._replace(query=urlencode(query_params, doseq=True))
    print("🔗 URL sem o parâmetro index:", urlunparse(parsed_url))
    return urlunparse(parsed_url)

def baixar_video(url):
    """Baixa vídeos, organizando playlists em pastas separadas."""
    url = remove_index_from_url(url)
    download_path = get_download_path()

    # Se for uma playlist, perguntar o nome da pasta e criar dentro de "vídeos baixados"
    if 'list=' in url:
        pasta_nome = input("📂 Insira o nome da pasta para salvar a playlist: ").strip()
        pasta_nome = sanitize_filename(pasta_nome)
        path = os.path.join(download_path, pasta_nome)  # Criar a pasta dentro de "vídeos baixados"
        os.makedirs(path, exist_ok=True)

        print(f"🎥 Playlist detectada! Baixando para a pasta: {path}")
        ydl_opts = {
            'format': 'bestaudio+bestevideo/best',  
            'outtmpl': f'{path}/%(playlist_index)s - %(title)s.%(ext)s',
            'restrictfilenames': True,
            'ignoreerrors': True,
            'merge_output_format': 'mp4',  
            'noplaylist': False,  
        }
    else:
        print("🎬 Vídeo único detectado! Baixando...")
        video_path = os.path.join(download_path, "Vídeos Soltos")  # Pasta para vídeos individuais
        os.makedirs(video_path, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio+bestevideo/best',  
            'outtmpl': f'{video_path}/%(title)s.%(ext)s',  
            'restrictfilenames': True,
            'ignoreerrors': True,
            'merge_output_format': 'mp4',  
            'noplaylist': True,  
        }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("✅ Download concluído!")
        except Exception as e:
            print("❌ Erro ao baixar:", e)

def main():
    url = input("🎥 Insira a URL do vídeo ou playlist do YouTube: ")
    baixar_video(url)

if __name__ == "__main__":
    main()
