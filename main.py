import tkinter as tk
from tkinter import Menu # Importar el widget Menu
from tkinter import ttk # Importar el widget ttk
from tkinter import messagebox
from app import monitorization
from app import panel_derecho
from app import panel_izquierdo
from app import pomodoro
import threading
import time
import datetime
import psutil
from app import scraping
from app import game
from app import gestor_tareas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
from app import graphics
from app import todo_list

def update_time(status_bar):
        while True:
            # Obtener la fecha y hora actual
            now = datetime.datetime.now()
            day_of_week = now.strftime("%A")  # Día de la semana
            time_str = now.strftime("%H:%M:%S")  # Hora en formato HH:MM:SS
            date_str = now.strftime("%Y-%m-%d")  # Fecha en formato YYYY-MM-DD
            label_text = f"{day_of_week}, {date_str} - {time_str}"

            # Actualizar el label (debemos usar `after` para asegurarnos que se actualice en el hilo principal de Tkinter)
            label_fecha_hora.after(1000, status_bar.config, {"text": label_text})

            # Espera 1 segundo antes de actualizar de nuevo
            time.sleep(1)
            
# Detener hilos de los graficos
def detener_aplicacion():
    graphics.detener_hilos()  # Detener los hilos de gráficos
    root.quit()      # Cerrar la ventana principal

# Crear la ventana principal
root = tk.Tk()
root.title("Ventana Responsive")
root.geometry("1000x700")  # Tamaño inicial

# Configurar la ventana principal para que sea responsive
root.columnconfigure(0, weight=0)  # Columna izquierda, tamaño fijo
root.columnconfigure(1, weight=1)  # Columna central, tamaño variable
root.columnconfigure(2, weight=0)  # Columna derecha, tamaño fijo
root.rowconfigure(0, weight=1)  # Fila principal, tamaño variable
root.rowconfigure(1, weight=0)  # Barra de estado, tamaño fijo

# Crear el menú superior
menu_bar = Menu(root)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nuevo")
file_menu.add_command(label="Abrir")
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Copiar")
edit_menu.add_command(label="Pegar")

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Acerca de")

menu_bar.add_cascade(label="Archivo", menu=file_menu)
menu_bar.add_cascade(label="Editar", menu=edit_menu)
menu_bar.add_cascade(label="Ayuda", menu=help_menu)

root.config(menu=menu_bar)

# Crear los frames laterales y el central
frame_izquierdo = tk.Frame(root, bg="lightgray", width=200)
frame_central = tk.Frame(root, bg="white")
frame_derecho = tk.Frame(root, bg="lightgray", width=200)

# Colocar los frames laterales y el central
frame_izquierdo.grid(row=0, column=0, sticky="ns")
frame_central.grid(row=0, column=1, sticky="nsew")
frame_derecho.grid(row=0, column=2, sticky="ns")

# Configurar los tamaños fijos de los frames laterales
frame_izquierdo.grid_propagate(False)
frame_derecho.grid_propagate(False)

# Dividir el frame central en dos partes (superior variable e inferior fija)
frame_central.rowconfigure(0, weight=1)  # Parte superior, tamaño variable
frame_central.rowconfigure(1, weight=0)  # Parte inferior, tamaño fijo
frame_central.columnconfigure(0, weight=1)  # Ocupa toda la anchura

# Crear subframes dentro del frame central
frame_superior = tk.Frame(frame_central, bg="lightyellow")
frame_inferior = tk.Frame(frame_central, bg="lightgray", height=250)

# Colocar los subframes dentro del frame central
frame_superior.grid(row=0, column=0, sticky="nsew")
frame_inferior.grid(row=1, column=0, sticky="ew")

# Fijar el tamaño de la parte inferior
frame_inferior.grid_propagate(False)

# Crear la barra de estado
barra_estado = tk.Label(root, text="Barra de estado", bg="lightgray", anchor="w")
barra_estado.grid(row=1, column=0, columnspan=3, sticky="ew")

# Notebook para las pestañas en el frame superior
style = ttk.Style()
style.configure("CustomNotebook.TNotebook.Tab", font=("Arial", 12, "bold"))
notebook = ttk.Notebook(frame_superior, style="CustomNotebook.TNotebook")
notebook.pack(fill="both", expand=True)

# Crear cinco solapas en el frame superior
for i in range(1, 6):
    tab = ttk.Frame(notebook)
    if i == 1:
        notebook.add(tab, text="Scrapping", padding=4)
        text_scrapping = tk.Text(tab, wrap="word")
        text_scrapping.pack(fill="both", expand=True)
    elif i == 2:  # Identificar la solapa 2
        notebook.add(tab, text="Pomodoro", padding=4)
        pomodoro.PomodoroTimer(tab)
    elif i == 3:
        notebook.add(tab, text="Gestor de tareas", padding=4)
        gestor_tareas.GestorTareas(tab)
    elif i == 4:
        notebook.add(tab, text='Juego', padding=4)
        game_frame = tk.Frame(tab)
        game_frame.pack(fill="both", expand=True)
        hilo_juego = game.HiloJuego(game_frame)
    elif i == 5:
        notebook.add(tab, text='To Do List', padding=4)
        todo_list.crear_solapa_todo(tab)

    else:
        notebook.add(tab, text=f"Solapa {i}", padding=4)
        # Añadir un Label en cada solapa para diferenciarla
        label = ttk.Label(tab, text=f"Contenido de la Solapa {i}")
        label.pack(pady=10)
      
# Notebook para las pestañas en el frame inferior
notebook_inferior = ttk.Notebook(frame_inferior, style="CustomNotebook.TNotebook")
notebook_inferior.pack(fill="both", expand=True)

# Pestaña de criptomonedas
tab_criptomonedas = ttk.Frame(notebook_inferior)
notebook_inferior.add(tab_criptomonedas, text="Gráfico Criptomonedas", padding=4)
fig_cripto, ax_cripto = plt.subplots(figsize=(8, 3))
canvas_cripto = FigureCanvasTkAgg(fig_cripto, tab_criptomonedas)
canvas_cripto.get_tk_widget().pack(fill="both", expand=True)

# Pestaña de IBEX
tab_ibex = ttk.Frame(notebook_inferior)
notebook_inferior.add(tab_ibex, text="Gráfico IBEX", padding=4)
fig_ibex, ax_ibex = plt.subplots(figsize=(8, 3))
canvas_ibex = FigureCanvasTkAgg(fig_ibex, tab_ibex)
canvas_ibex.get_tk_widget().pack(fill="both", expand=True)

# Iniciar los hilos para los gráficos
graphics.iniciar_hilos(canvas_cripto, ax_cripto, canvas_ibex, ax_ibex)


# Barra de estado dividida
label_cpu_used = tk.Label(barra_estado, text="CPU: 0%", font=("Helvetica", 11), bd=1, fg="blue", relief="sunken", anchor="w", width=20, padx=10)
label_ram_used = tk.Label(barra_estado, text="RAM: 0%", font=("Helvetica", 11), bd=1, fg="blue", relief="sunken", anchor="w", width=20, padx=10)
label_pc_battery = tk.Label(barra_estado, text="Temperatura CPU: ", font=("Helvetica", 11), bd=1, fg="blue", relief="sunken", anchor="w", width=20, padx=10)
label_network_used = tk.Label(barra_estado, text="Red: ", font=("Helvetica", 11), bd=1, fg="blue", relief="sunken", anchor="w", width=20, padx=10)
label_fecha_hora = tk.Label(barra_estado, text="Hilo fecha-hora", font=("Helvetica", 11), bd=1, fg="blue", relief="sunken", anchor="w", width=20, padx=10)

label_cpu_used.pack(side="left", fill="x", expand=True)
label_ram_used.pack(side="left", fill="x", expand=True)
label_pc_battery.pack(side="left", fill="x", expand=True)
label_network_used.pack(side="left", fill="x", expand=True)
label_fecha_hora.pack(side="right", fill="x", expand=True)

# Monitorización barra horizontal de abajo
update_thread = threading.Thread(target=update_time, args=(label_fecha_hora,))
update_thread.daemon = True  
update_thread.start()

thread_cpu_monitor = threading.Thread(target=monitorization.monitor_cpu_usage, args=(label_cpu_used,))
thread_cpu_monitor.daemon = True  
thread_cpu_monitor.start()

thread_ram_monitor = threading.Thread(target=monitorization.monitor_ram_usage, args=(label_ram_used,))
thread_ram_monitor.daemon = True
thread_ram_monitor.start()

thread_temperature_battery = threading.Thread(target=monitorization.monitor_battery, args=(label_pc_battery,))
thread_temperature_battery.daemon = True
thread_temperature_battery.start()

thread_network_used_monitor = threading.Thread(target=monitorization.monitor_network_usage, args=(label_network_used,))
thread_network_used_monitor.daemon = True
thread_network_used_monitor.start()

# Lados verticales
panel_d = panel_derecho.PanelDerecho(frame_derecho)
panel_i = panel_izquierdo.PanelIzquierdo(frame_izquierdo,  text_scrapping) 

root.protocol("WM_DELETE_WINDOW", detener_aplicacion)

# Ejecución de la aplicación
root.mainloop()
