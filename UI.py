import tkinter as tk
from tkinter import filedialog

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")
        self.root.geometry("600x400")

        # Configuración de colores
        bg_color = "#2E2E2E"
        fg_color = "#FFFFFF"

        self.root.configure(bg=bg_color)

        # Barra de menú
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Menú Archivo
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.destroy)

        # Frame principal
        main_frame = tk.Frame(self.root, bg=bg_color)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Lista de archivos
        file_listbox = tk.Listbox(main_frame, bg=bg_color, fg=fg_color)
        file_listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(title="Abrir archivo", filetypes=[("Archivos de texto", "*.txt")])
        # Puedes agregar lógica para manejar el archivo abierto según tus necesidades

    def save_file(self):
        file_path = filedialog.asksaveasfilename(title="Guardar archivo", defaultextension=".txt",
                                                   filetypes=[("Archivos de texto", "*.txt")])
        # Puedes agregar lógica para manejar el archivo guardado según tus necesidades


if __name__ == "__main__":
    root = tk.Tk()
    file_explorer = FileExplorer(root)
    root.mainloop()
