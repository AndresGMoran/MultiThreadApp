import tkinter as tk
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO
from app import scraping

class PanelIzquierdo:
    def __init__(self, frame, text_widget):
        # Configuración del panel
        self.frame = frame
        self.frame.configure(bg="lightblue", width=200)
        self.frame.grid_propagate(False)
        self.frame.columnconfigure(0, weight=1)

        # Sección: Clima
        clima_frame = tk.Frame(self.frame, bg="white", bd=2, relief="sunken")
        clima_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        clima_title = tk.Label(clima_frame, text="Clima Actual", bg="white", font=("Helvetica", 12, "bold"), fg="navy")
        clima_title.pack(pady=5)

        self.weather_icon = tk.Label(clima_frame, bg="white")
        self.weather_icon.pack()

        self.weather_label = tk.Label(clima_frame, text="Cargando clima...", bg="white", font=("Helvetica", 10), fg="black")
        self.weather_label.pack(pady=5)
        self.update_weather()

        # Sección: Scrapping
        scraping_frame = tk.Frame(self.frame, bg="white", bd=2, relief="sunken")
        scraping_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        scraping_title = tk.Label(scraping_frame, text="Scraping", bg="white", font=("Helvetica", 12, "bold"), fg="navy")
        scraping_title.pack(pady=5)

        boton_scrapping = tk.Button(
            scraping_frame,
            text="Iniciar Scrapping",
            command=lambda: threading.Thread(
                target=scraping.iniciar_scraping_y_insercion,
                args=("https://www.amazon.es/", text_widget)
            ).start(),
            bg="lightgreen"
        )
        boton_scrapping.pack(pady=5)

        # Sección: Noticias
        noticias_frame = tk.Frame(self.frame, bg="white", bd=2, relief="sunken")
        noticias_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        noticias_title = tk.Label(noticias_frame, text="Últimas Noticias", bg="white", font=("Helvetica", 12, "bold"), fg="navy")
        noticias_title.pack(pady=5)

        self.news_label = tk.Label(
            noticias_frame, text="Cargando noticias...", bg="white", font=("Helvetica", 10), fg="black", wraplength=180, justify="left"
        )
        self.news_label.pack(pady=5)
        self.update_news()

        # Configuración para que las filas crezcan dinámicamente
        self.frame.rowconfigure(2, weight=1)

    def update_weather(self):
        """Actualiza la información del clima utilizando un hilo."""
        def fetch_weather():
            try:
                url = f'http://api.openweathermap.org/data/2.5/weather?q=Javea&appid=key&units=metric&lang=es'
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                # Información del clima
                temp = data['main']['temp']
                weather = data['weather'][0]['description']
                icon_code = data['weather'][0]['icon']

                # Actualiza el texto del clima
                self.weather_label.config(
                    text=f"Javea:\n{temp}°C, {weather.capitalize()}"
                )

                # Descarga y muestra el ícono del clima
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                icon_response = requests.get(icon_url)
                icon_image = Image.open(BytesIO(icon_response.content))
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.weather_icon.config(image=icon_photo)
                self.weather_icon.image = icon_photo  # Referencia para evitar que se elimine

            except Exception as e:
                self.weather_label.config(text="Error al obtener el clima.")
                print(f"Error al obtener el clima: {e}")

        threading.Thread(target=fetch_weather, daemon=True).start()

    def update_news(self):
        """Consulta y actualiza las últimas noticias en tiempo real."""
        def fetch_news():
            while True:
                try:
                    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=key'
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()

                    articles = data['articles'][:7]  # Obtiene las 5 primeras noticias
                    news_text = "\n\n".join([f"- {article['title']}" for article in articles])
                    self.news_label.config(text=news_text)
                except Exception as e:
                    self.news_label.config(text="Error al obtener noticias")
                    print(f"Error al obtener noticias: {e}")

        threading.Thread(target=fetch_news, daemon=True).start()
