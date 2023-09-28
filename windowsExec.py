import os
import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import validators
import re
from ttkthemes import ThemedTk


class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to MP3 Converter")

        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        self.root.set_theme("radiance")

        title_label = ttk.Label(
            frame, text="Video to MP3 Converter", font=("Helvetica", 16, "bold"))
        title_label.pack()

        url_label = ttk.Label(frame, text="Insira o link do vídeo:")
        url_label.pack()

        self.url_entry = ttk.Entry(frame)
        self.url_entry.pack(fill=tk.X)

        destination_label = ttk.Label(
            frame, text="Insira o caminho de destino:")
        destination_label.pack()

        self.destination_entry = ttk.Entry(frame)
        self.destination_entry.pack(fill=tk.X)

        self.format_var = tk.BooleanVar()
        format_check = ttk.Checkbutton(
            frame, text="Converter para MP3", variable=self.format_var)
        format_check.pack()

        self.download_button = ttk.Button(
            frame, text="Baixar e Converter", command=self.download_and_convert)
        self.download_button.pack()

        # Aviso de Direitos Autorais
        copyright_label = ttk.Label(
            frame, text="@Mello - Todos os direitos reservados", font=("Helvetica", 8))
        # Move para a parte inferior
        copyright_label.pack(side=tk.BOTTOM, pady=10)

        self.progress_bar = ttk.Progressbar(
            frame, orient="horizontal", mode="determinate")
        # Move para a parte inferior
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    def download_and_convert(self):
        video_url = self.url_entry.get()
        destination_path = self.destination_entry.get()

        try:
            if not validators.url(video_url):
                self.log("URL inválida.")
                messagebox.showerror("Erro", "URL inválida.")
                return

            yt = YouTube(video_url)
            self.log("Título do vídeo:", yt.title)

            # Remover caracteres inválidos do nome do arquivo
            cleaned_title = re.sub(r'[\/:*?"<>|]', '', yt.title)
            video_filename = cleaned_title + ".mp4"
            download_path = os.path.join(destination_path, video_filename)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=destination_path,
                            filename=video_filename)

            self.progress_bar["maximum"] = 100
            self.progress_bar["value"] = 50

            if self.format_var.get():
                mp3_filename = cleaned_title + ".mp3"
                mp3_path = os.path.join(destination_path, mp3_filename)
                ffmpeg_extract_audio(download_path, mp3_path)
                os.remove(download_path)

            self.progress_bar["value"] = 100
            messagebox.showinfo("Sucesso", "Download e conversão concluídos!")

            # Reset da barra de carregamento após a conclusão
            self.progress_bar["value"] = 0

        except Exception as e:
            self.log("Ocorreu um erro:", e)
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def log(self, *args):
        print("LOG:", *args)


def main():
    root = ThemedTk(theme="radiance")
    app = VideoConverterApp(root)
    root.geometry("400x350")
    root.mainloop()


if __name__ == "__main__":
    main()
