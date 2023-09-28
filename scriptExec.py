import os
import re
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import validators


def download_and_convert_video():
    try:
        video_url = input("Insira o link do vídeo: ")
        if not validators.url(video_url):
            print("URL inválida.")
            return

        yt = YouTube(video_url)
        print("Título do vídeo:", yt.title)

        # Preencha o caminho de download desejado ou mantenha em branco para baixar no diretorio atual
        destination_path = input("")
        if not destination_path:
            destination_path = os.getcwd()

        format_choice = input("Escolha o formato (1 = MP3, 2 = MP4): ")
        if format_choice not in ['1', '2']:
            print("Escolha inválida.")
            return

        format_mp3 = (format_choice == '1')

        # Remover caracteres inválidos do nome do arquivo
        cleaned_title = re.sub(r'[\/:*?"<>|]', '', yt.title)
        video_filename = cleaned_title + ".mp4"
        download_path = os.path.join(destination_path, video_filename)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=destination_path, filename=video_filename)

        if format_mp3:
            mp3_filename = cleaned_title + ".mp3"
            mp3_path = os.path.join(destination_path, mp3_filename)
            ffmpeg_extract_audio(download_path, mp3_path)
            os.remove(download_path)

        print("Download e conversão concluídos!")

    except Exception as e:
        print("Ocorreu um erro:", e)


if __name__ == "__main__":
    download_and_convert_video()
