import requests
import yfinance as yf
import threading
import random
import time

running = True  


def actualizar_grafico_criptomonedas_api(canvas, ax):
    """Actualiza los datos del gráfico de criptomonedas utilizando CoinGecko API."""
    while True:
        if not running:  # Verifica si el programa está en ejecución
            break
        if not canvas.get_tk_widget().winfo_exists():  
            break
        try:
            # Solicitar datos de precios de criptomonedas
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Obtener precios actuales
            bitcoin_price = data['bitcoin']['usd']
            ethereum_price = data['ethereum']['usd']

            # Actualizar el gráfico con datos simulados + precios reales
            ax.clear()
            ax.set_title("Gráfico Criptomonedas")
            ax.plot([random.randint(1, 100) for _ in range(10)], label=f"Bitcoin (${bitcoin_price})", color="blue")
            ax.plot([random.randint(1, 100) for _ in range(10)], label=f"Ethereum (${ethereum_price})", color="green")
            ax.legend()
            canvas.draw()
        except Exception as e:
            print(f"Error al obtener datos de criptomonedas: {e}")
        time.sleep(60)  


def actualizar_grafico_ibex_api(canvas, ax):
    """Actualiza los datos del gráfico del IBEX utilizando Yahoo Finance API."""
    while True:
        if not running:  # Verifica si el programa está en ejecución
            break
        if not canvas.get_tk_widget().winfo_exists():  
            break
        try:
            # Obtener datos históricos de IBEX 35
            data = yf.Ticker("^IBEX").history(period="1d", interval="5m")

            close_prices = data['Close'].values

            # Actualizar el gráfico con los datos reales
            ax.clear()
            ax.set_title("Gráfico IBEX")
            ax.plot(close_prices, label="IBEX", color="orange")
            ax.legend()
            canvas.draw()
        except Exception as e:
            print(f"Error al obtener datos del IBEX: {e}")
        time.sleep(60) 


def iniciar_hilos(canvas_cripto, ax_cripto, canvas_ibex, ax_ibex):
    """Inicia los hilos de actualización de gráficos."""
    global running
    running = True 

    # Hilo para criptomonedas
    thread_criptomonedas = threading.Thread(
        target=actualizar_grafico_criptomonedas_api, args=(canvas_cripto, ax_cripto), daemon=True
    )
    thread_criptomonedas.start()

    # Hilo para IBEX
    thread_ibex = threading.Thread(
        target=actualizar_grafico_ibex_api, args=(canvas_ibex, ax_ibex), daemon=True
    )
    thread_ibex.start()


def detener_hilos():
    """Detiene la ejecución de los hilos."""
    global running
    running = False
    print("Hilos detenidos.")
