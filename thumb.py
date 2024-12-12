import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from io import BytesIO
import requests
import re
import os

# Função para baixar a thumbnail
def download_youtube_thumbnail(video_url, image_label):
    # Regex para extrair o ID do vídeo do URL
    video_id_match = re.search(r"(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})", video_url)
    if not video_id_match:
        messagebox.showerror("Erro", "URL inválido. Certifique-se de fornecer um link válido do YouTube.")
        return

    video_id = video_id_match.group(1)
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

    try:
        # Baixar a thumbnail
        response = requests.get(thumbnail_url)
        response.raise_for_status()  # Verificar se houve erros no download

        # Solicitar ao usuário onde salvar o arquivo
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if not save_path:
            return  # O usuário cancelou a seleção

        # Salvar a thumbnail no local escolhido
        with open(save_path, "wb") as file:
            file.write(response.content)

        # Exibir a imagem na GUI
        img_data = BytesIO(response.content)
        img = Image.open(img_data).resize((320, 180), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo

        # Ajustando o tamanho do label para o tamanho da imagem
        image_label.config(width=img.width, height=img.height)

        # Informar o usuário
        messagebox.showinfo("Sucesso", f"Thumbnail baixada e salva em: {save_path}")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao baixar a thumbnail: {e}")

# Função para limpar os campos
def clear_fields(url_entry, image_label):
    url_entry.delete(0, tk.END)
    image_label.config(image='')

# Função para sair
def close_app(window):
    window.quit()

# Função para trocar o tema
def change_theme(window, theme):
    ttk.Style().theme_use(theme)
    window.config(bg="#2e2e2e")

# Função para centralizar a janela na tela
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

# Criando a interface principal
def create_gui():
    # Configuração da janela principal
    window = tk.Tk()
    window.title("Baixador de Thumbnails do YouTube")
    window.config(bg="#2e2e2e")

    # Centralizar a janela
    window_width = 600
    window_height = 400
    center_window(window, window_width, window_height)

    # Estilo escuro
    style = ttk.Style()
    style.configure("TButton", background="#3a3a3a", foreground="white", font=("Arial", 12))
    style.configure("TLabel", background="#2e2e2e", foreground="white", font=("Arial", 12))
    style.configure("TEntry", fieldbackground="#4a4a4a", foreground="white", font=("Arial", 12))

    # Barra de título
    title_label = ttk.Label(window, text="Baixador de Thumbnails do YouTube", font=("Arial", 18, "bold"), anchor="center")
    title_label.grid(row=0, column=0, columnspan=3, pady=20)

    # Entrada de URL
    url_label = ttk.Label(window, text="Insira o URL do vídeo do YouTube:")
    url_label.grid(row=1, column=0, padx=20, pady=10)

    url_entry = ttk.Entry(window, width=50)
    url_entry.grid(row=1, column=1, padx=20, pady=10)

    # Exibição da imagem (Usando tk.Label em vez de ttk.Label)
    image_label = tk.Label(window, width=40, height=20, relief="solid", background="lightgray")
    image_label.grid(row=2, column=0, columnspan=3, pady=20)

    # Botões para baixar, limpar e sair
    button_frame = ttk.Frame(window)
    button_frame.grid(row=3, column=0, columnspan=3, pady=10)

    download_button = ttk.Button(button_frame, text="Baixar Thumbnail", width=20, command=lambda: download_youtube_thumbnail(url_entry.get(), image_label))
    download_button.grid(row=0, column=0, padx=10)

    clear_button = ttk.Button(button_frame, text="Limpar", width=20, command=lambda: clear_fields(url_entry, image_label))
    clear_button.grid(row=0, column=1, padx=10)

    exit_button = ttk.Button(button_frame, text="Sair", width=20, command=lambda: close_app(window))
    exit_button.grid(row=0, column=2, padx=10)

    # Botão para mudar o tema
    theme_button = ttk.Button(window, text="Alterar Tema", width=20, command=lambda: change_theme(window, "clam"))
    theme_button.grid(row=4, column=0, columnspan=3, pady=10)

    # Rodando a interface
    window.mainloop()

# Iniciar a GUI
if __name__ == "__main__":
    create_gui()
