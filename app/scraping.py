import requests
from bs4 import BeautifulSoup
import threading
import mysql.connector  
from queue import Queue

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',  
            port=3306,
            user='root',  
            password='1234', 
            database='scraping'  
        )
        return conexion
    except mysql.connector.Error as err:  
        print(f"Error al conectar con la base de datos: {err}")
        return None


# Función para extraer enlaces y enviarlos a la cola
def extraer_enlaces(url, cola, text_widget):
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            contenido_html = respuesta.text
            soup = BeautifulSoup(contenido_html, 'html.parser')
            for enlace in soup.find_all('a', href=True):
                enlace_str = enlace['href']
                cola.put(enlace_str)  
                if text_widget:  
                    text_widget.insert('end', enlace_str + "\n")
            print("Extracción de enlaces completada.")
        else:
            print(f"Error al acceder a la URL: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error durante la solicitud HTTP: {e}")

# Función para insertar enlaces en la base de datos
def insertar_enlaces_mysql(cola):
    conexion = obtener_conexion()
    if not conexion:
        return

    cursor = conexion.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS enlaces (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        enlace VARCHAR(255) UNIQUE
                    )''')

    while True:
        enlace = cola.get()  
        if enlace == "FIN":
            break 

        try:
            cursor.execute("INSERT IGNORE INTO enlaces (enlace) VALUES (%s)", (enlace,))
            conexion.commit()
            print(f"Enlace insertado en la base de datos: {enlace}")
        except mysql.connector.Error as err:  
            print(f"Error al insertar enlace: {err}")

    cursor.close()
    conexion.close()
    print("Inserción en la base de datos finalizada.")


# Función para iniciar el scraping y la inserción en hilos
def iniciar_scraping_y_insercion(url, text_widget):
    cola_enlaces = Queue()
    # Configurar los hilos como daemon
    hilo_scraping = threading.Thread(target=extraer_enlaces, args=(url, cola_enlaces, text_widget), daemon=True)
    hilo_insercion = threading.Thread(target=insertar_enlaces_mysql, args=(cola_enlaces,), daemon=True)
    hilo_scraping.start()
    hilo_insercion.start()
    hilo_scraping.join()
    cola_enlaces.put("FIN")
    hilo_insercion.join()