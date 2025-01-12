from tkinter import messagebox
import threading
import time
import datetime
import psutil

def monitor_cpu_usage(label):
    """Monitorea y actualiza el uso de CPU en tiempo real."""
    while True:
        if not label.winfo_exists():  # Verifica si el Label existe
            break
        cpu_percent = psutil.cpu_percent(interval=1)  # Obtiene el uso de CPU cada segundo
        label.config(text=f"CPU: {cpu_percent}%")
        time.sleep(1)

def monitor_ram_usage(label):
    """Monitorea y actualiza el uso de RAM en tiempo real."""
    while True:
        if not label.winfo_exists():  # Verifica si el Label existe
            break
        memory_info = psutil.virtual_memory()
        ram_percent = memory_info.percent  # Porcentaje de uso de RAM
        label.config(text=f"RAM: {ram_percent}%")
        time.sleep(1)


def monitor_battery(label):
    """Monitorea el estado de la batería y actualiza un label."""
    low_battery_alert_shown = False  # Bandera para evitar múltiples alertas
    
    while True:
        if not label.winfo_exists():  # Verifica si el Label existe
            break
        try:
            # Obtiene la información de la batería
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                charging = "Cargando" if battery.power_plugged else "Descargando"
                
                # Validar el tiempo restante
                if battery.secsleft == psutil.POWER_TIME_UNKNOWN or battery.secsleft < 0:
                    time_left_str = "Calculando..."
                else:
                    hours = battery.secsleft // 3600
                    minutes = (battery.secsleft % 3600) // 60
                    time_left_str = f"{hours}h {minutes}m"

                # Mostrar alerta si la batería es menor o igual al 15% y no está cargando
                if percent <= 15 and not battery.power_plugged and not low_battery_alert_shown:
                    low_battery_alert_shown = True
                    label.after(0, lambda: messagebox.showwarning(
                        "Batería Baja",
                        "El nivel de batería está por debajo del 15%. Por favor, conecta el cargador."
                    ))

                # Resetear la bandera si se conecta el cargador
                if battery.power_plugged:
                    low_battery_alert_shown = False

                label.after(0, lambda: label.config(
                    text=f"Batería: {percent}% - {charging} - {time_left_str} restantes"
                ))
            else:
                # Si no hay batería, mostrar un mensaje
                label.after(0, lambda: label.config(text="Batería: No disponible"))

        except Exception as e:
            label.after(0, lambda: label.config(text=f"Error: {str(e)[:30]}..."))

        time.sleep(5)  # Actualiza cada 5 segundos

def monitor_network_usage(label):
    """Monitorea y actualiza el uso de la red en tiempo real."""
    prev_net = psutil.net_io_counters()
    while True:
        if not label.winfo_exists():  # Verifica si el Label existe
            break
        time.sleep(1)  # Intervalo de actualización
        current_net = psutil.net_io_counters()
        sent = (current_net.bytes_sent - prev_net.bytes_sent) / (1024 * 1024)  # En MB
        recv = (current_net.bytes_recv - prev_net.bytes_recv) / (1024 * 1024)  # En MB
        prev_net = current_net
        label.config(text=f"Red: Enviado {sent:.2f} MB, Recibido {recv:.2f} MB")
