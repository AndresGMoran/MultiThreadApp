import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time


class PomodoroTimer:
    def __init__(self, parent):
        self.parent = parent
        self.work_time = 25 * 60  
        self.break_time = 5 * 60  
        self.remaining_time = self.work_time
        self.is_running = False
        self.is_break = False
        self.timer_thread = None

        # Interfaz del Pomodoro
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(fill="both", expand=True)

        # Título del temporizador
        self.title_label = tk.Label(
            self.frame, text="Pomodoro Timer", font=("Helvetica", 18, "bold"), bg="white", fg="#ff6347"
        )
        self.title_label.pack(pady=20)

        # Barra de progreso
        self.progress = ttk.Progressbar(self.frame, maximum=self.work_time, length=300)
        self.progress.pack(pady=10)

        # Label del temporizador
        self.timer_label = tk.Label(
            self.frame, text=self.format_time(self.remaining_time), font=("Helvetica", 36, "bold"), bg="white", fg="#4caf50"
        )
        self.timer_label.pack(pady=10)

        # Contenedor para botones
        button_frame = tk.Frame(self.frame, bg="white")
        button_frame.pack(pady=20)

        self.start_button = tk.Button(
            button_frame, text="Iniciar", command=self.start_timer, bg="#4caf50", fg="white", font=("Helvetica", 12, "bold"), width=10
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(
            button_frame, text="Pausar", command=self.pause_timer, bg="#ff9800", fg="white", font=("Helvetica", 12, "bold"), width=10
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(
            button_frame, text="Reiniciar", command=self.reset_timer, bg="#f44336", fg="white", font=("Helvetica", 12, "bold"), width=10
        )
        self.reset_button.grid(row=0, column=2, padx=5)

        # Configuración de tiempos
        settings_frame = tk.Frame(self.frame, bg="white")
        settings_frame.pack(pady=20)

        self.settings_label = tk.Label(
            settings_frame, text="Configurar tiempos (min):", font=("Helvetica", 10), bg="white"
        )
        self.settings_label.grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(settings_frame, text="Trabajo:", font=("Helvetica", 10), bg="white").grid(row=1, column=0, pady=5)
        self.work_time_entry = tk.Entry(settings_frame, width=5, justify="center")
        self.work_time_entry.insert(0, "25")
        self.work_time_entry.grid(row=1, column=1, pady=5)

        tk.Label(settings_frame, text="Descanso:", font=("Helvetica", 10), bg="white").grid(row=2, column=0, pady=5)
        self.break_time_entry = tk.Entry(settings_frame, width=5, justify="center")
        self.break_time_entry.insert(0, "5")
        self.break_time_entry.grid(row=2, column=1, pady=5)

        self.apply_button = tk.Button(
            settings_frame, text="Aplicar", command=self.apply_settings, bg="#2196f3", fg="white", font=("Helvetica", 10, "bold")
        )
        self.apply_button.grid(row=3, column=0, columnspan=2, pady=10)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()

    def pause_timer(self):
        self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.remaining_time = self.work_time if not self.is_break else self.break_time
        self.update_timer_label()
        self.progress["value"] = 0  
        self.progress["maximum"] = 100  

    def apply_settings(self):
        try:
            work_minutes = int(self.work_time_entry.get())
            break_minutes = int(self.break_time_entry.get())
            self.work_time = work_minutes * 60
            self.break_time = break_minutes * 60
            self.reset_timer()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

    def run_timer(self):
        total_time = self.remaining_time  # Guarda el tiempo total inicial
        while self.remaining_time > 0 and self.is_running:
            time.sleep(1)
            self.remaining_time -= 1
            self.update_timer_label()
            # Calcula el progreso como porcentaje
            elapsed_time = total_time - self.remaining_time
            progress_value = (elapsed_time / total_time) * 100
            self.progress["value"] = progress_value

        if self.remaining_time == 0 and self.is_running:
            self.is_running = False
            self.is_break = not self.is_break
            self.remaining_time = self.break_time if self.is_break else self.work_time
            self.progress["maximum"] = 100 
            self.update_timer_label()
            self.progress["value"] = 0  
            messagebox.showinfo(
                "Pomodoro Finalizado",
                "¡Tiempo de descanso!" if self.is_break else "¡Tiempo de trabajar!",
            )
            if self.is_running:
                self.start_timer()



    def update_timer_label(self):
        self.timer_label.config(text=self.format_time(self.remaining_time))

    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"
