import pygame
import threading
import random
import time
import tkinter as tk
from tkinter import Frame, Canvas, messagebox, Button

class HiloJuego:
    def __init__(self, parent):
        self.parent = parent
        self.running = False
        self.score = 0
        self.misses = 0  # Contador de fallos
        self.max_misses = 3  # Número máximo de fallos permitidos
        self.circles = []

        # Crear el canvas dentro del frame proporcionado
        self.canvas = Canvas(parent, width=200, height=100, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Crear botón para iniciar el juego
        self.start_button = Button(parent, text="Iniciar Juego", command=self.start_game)
        self.start_button.pack(pady=10)

    class Circle:
        def __init__(self, x, y, radius, duration):
            self.x = x
            self.y = y
            self.radius = radius
            self.duration = duration
            self.appeared_at = time.time()

        def is_expired(self):
            return time.time() - self.appeared_at > self.duration

    def generate_circles(self):
        while self.running:
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            radius = 40
            duration = random.uniform(1.5, 3.0)
            circle = self.Circle(x, y, radius, duration)
            self.circles.append(circle)
            time.sleep(random.uniform(0.5, 1.5))

    def main_loop(self):
        self.canvas.bind("<Button-1>", self.on_click)

        # Inicia el hilo para generar círculos
        circle_thread = threading.Thread(target=self.generate_circles)
        circle_thread.daemon = True
        circle_thread.start()

        while self.running:
            self.canvas.delete("all")

            # Dibujar círculos
            for circle in self.circles[:]:
                if circle.is_expired():
                    self.circles.remove(circle)
                    self.misses += 1
                    if self.misses >= self.max_misses:
                        self.end_game()
                        return
                else:
                    self.canvas.create_oval(
                        circle.x - circle.radius, circle.y - circle.radius,
                        circle.x + circle.radius, circle.y + circle.radius,
                        outline="red", width=3
                    )

            # Mostrar puntaje y fallos
            self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", fill="white", font=("Arial", 16))
            self.canvas.create_text(10, 40, anchor="nw", text=f"Misses: {self.misses}/{self.max_misses}", fill="white", font=("Arial", 16))

            self.canvas.update()
            time.sleep(0.016)

    def on_click(self, event):
        if not self.running:
            return
        x, y = event.x, event.y
        hit = False
        for circle in self.circles[:]:
            if (x - circle.x) ** 2 + (y - circle.y) ** 2 <= circle.radius ** 2:
                self.score += 1
                self.circles.remove(circle)
                hit = True
                break
        if not hit:
            self.misses += 1
            if self.misses >= self.max_misses:
                self.end_game()

    def start_game(self):
        if not self.running:
            self.running = True
            self.score = 0
            self.misses = 0
            self.circles = []
            self.start_button.pack_forget()  # Ocultar el botón al iniciar el juego
            game_thread = threading.Thread(target=self.main_loop)
            game_thread.daemon = True
            game_thread.start()

    def end_game(self):
        self.running = False
        messagebox.showinfo("Game Over", f"Has perdido. Puntaje final: {self.score}")
        self.start_button.pack(pady=10)  # Mostrar el botón nuevamente al finalizar el juego

    def stop(self):
        self.running = False
