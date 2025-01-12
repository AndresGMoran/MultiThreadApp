import tkinter as tk
from tkinter import ttk
import threading
import psutil
import time

class GestorTareas:
    def __init__(self, frame):
        self.frame = frame

        # Configurar estilo para ttk.Frame
        style = ttk.Style()
        style.configure("Custom.TFrame", background="white")
        self.frame.configure(style="Custom.TFrame")

        # Título
        self.title_label = ttk.Label(
            self.frame, text="Administrador de Tareas", font=("Helvetica", 16, "bold"), background="white"
        )
        self.title_label.pack(pady=10)

        # Tabla de procesos
        self.processes_frame = ttk.Frame(self.frame)
        self.processes_frame.pack(fill="both", expand=True)

        self.processes_list = tk.Listbox(self.processes_frame, width=80, height=20)
        self.processes_list.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(self.processes_frame, orient="vertical", command=self.processes_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.processes_list.config(yscrollcommand=scrollbar.set)

        # Botón para actualizar procesos
        self.update_button = ttk.Button(
            self.frame, text="Actualizar", command=self.start_updating_processes
        )
        self.update_button.pack(pady=10)

    def start_updating_processes(self):
        threading.Thread(target=self.update_processes, daemon=True).start()

    def update_processes(self):
        while True:
            self.processes_list.delete(0, tk.END)
            for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    process_info = (
                        f"PID: {proc.info['pid']} | Nombre: {proc.info['name']} | "
                        f"CPU: {proc.info['cpu_percent']}% | Memoria: {proc.info['memory_info'].rss / (1024 ** 2):.2f} MB"
                    )
                    self.processes_list.insert(tk.END, process_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            time.sleep(5)
