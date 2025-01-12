import tkinter as tk
from tkinter import messagebox
import threading
import pygame  # Para reproducir música


class PanelDerecho:
    def __init__(self, frame):
        # Inicializar el reproductor de música
        pygame.mixer.init()

        # Asociar el frame del panel derecho
        self.frame = frame
        self.frame.configure(bg="lightblue", width=200)
        self.frame.grid_propagate(False)
        self.frame.columnconfigure(0, weight=1)

        # Título del chat
        chat_label = tk.Label(self.frame, text="Chat", font=("Helvetica", 12, "bold"), bg="white", fg="red")
        chat_label.grid(row=0, column=0, sticky="ew", pady=5, padx=5)

        # Área de entrada de mensaje
        mensaje_label = tk.Label(self.frame, text="Mensaje", font=("Helvetica", 10), bg="lightblue")
        mensaje_label.grid(row=1, column=0, sticky="w", padx=5)
        self.entrada_mensaje = tk.Text(self.frame, height=5, bg="lightyellow", wrap="word")
        self.entrada_mensaje.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # Botón de enviar 
        boton_enviar = tk.Button(self.frame, text="Enviar", bg="lightgreen", command=self.enviar_mensaje_thread)
        boton_enviar.grid(row=3, column=0, pady=5, padx=5, sticky="ew")

        # Listado de mensajes
        mensajes_frame = tk.Frame(self.frame, bg="white", bd=2, relief="sunken")
        mensajes_frame.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        mensajes_frame.columnconfigure(0, weight=1)
        self.mensajes_frame = mensajes_frame

        # Mensajes iniciales
        self.mensajes = [
            {"alumno": "Alumno 1", "texto": "Voy to mal con el trabajo final de DAM, pero seguro que chatgpt me lo hace en nada asiq de chill."},
            {"alumno": "Alumno 2", "texto": "Me puedes pasar el ultimo trabajo porfa, es que no me a dado tiempo."},
        ]
        self.actualizar_mensajes()

        # Reproductor de música
        musica_frame = tk.Frame(self.frame, bg="lightgray", height=50)
        musica_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        tk.Label(musica_frame, text="Reproductor música", bg="lightgray", font=("Helvetica", 10)).pack()

        # Botones de control de música
        boton_play = tk.Button(musica_frame, text="Play", bg="green", fg="white", command=self.reproducir_musica_thread)
        boton_play.pack(side="left", padx=5)

        boton_pause = tk.Button(musica_frame, text="Pause", bg="orange", fg="white", command=self.pausar_musica_thread)
        boton_pause.pack(side="left", padx=5)

        boton_restart = tk.Button(musica_frame, text="Restart", bg="blue", fg="white", command=self.reiniciar_musica_thread)
        boton_restart.pack(side="left", padx=5)

        self.frame.rowconfigure(4, weight=1)  

    #Metodos para mensajes
    def enviar_mensaje_thread(self):
        """Inicia un hilo para agregar un mensaje."""
        threading.Thread(target=self.enviar_mensaje, daemon=True).start()

    def enviar_mensaje(self):
        """Agrega un mensaje al listado."""
        texto = self.entrada_mensaje.get("1.0", tk.END).strip()
        if texto:
            self.mensajes.append({"alumno": "Tú", "texto": texto})
            self.entrada_mensaje.delete("1.0", tk.END)
            self.actualizar_mensajes()
        else:
            messagebox.showwarning("Aviso", "El mensaje está vacío.")

    def actualizar_mensajes(self):
        """Actualiza el listado de mensajes en la interfaz."""
        for widget in self.mensajes_frame.winfo_children():
            widget.destroy() 

        for mensaje in self.mensajes:
            tk.Label(self.mensajes_frame, text=mensaje["alumno"], font=("Helvetica", 10, "bold"), anchor="w").pack(
                fill="x", padx=5, pady=2
            )
            tk.Label(
                self.mensajes_frame, text=mensaje["texto"], font=("Helvetica", 9), anchor="w", wraplength=180, justify="left"
            ).pack(fill="x", padx=5, pady=2)

    # Metodos para control de música
    def reproducir_musica_thread(self):
        """Inicia un hilo para reproducir música."""
        threading.Thread(target=self.reproducir_musica, daemon=True).start()

    def reproducir_musica(self):
        """Reproduce una canción."""
        try:
            pygame.mixer.music.load("cancion.mp3") 
            pygame.mixer.music.play()
            messagebox.showinfo("Reproducción", "Reproduciendo canción.")
        except pygame.error as e:
            messagebox.showerror("Error", f"No se pudo reproducir la canción: {e}")

    def pausar_musica_thread(self):
        """Inicia un hilo para pausar la música."""
        threading.Thread(target=self.pausar_musica, daemon=True).start()

    def pausar_musica(self):
        """Pausa la música."""
        pygame.mixer.music.pause()
        messagebox.showinfo("Reproducción", "Música en pausa.")

    def reiniciar_musica_thread(self):
        """Inicia un hilo para reiniciar la música."""
        threading.Thread(target=self.reiniciar_musica, daemon=True).start()

    def reiniciar_musica(self):
        """Reinicia la música desde el principio."""
        pygame.mixer.music.stop()
        pygame.mixer.music.play()
        messagebox.showinfo("Reproducción", "Reproduciendo desde el principio.")
