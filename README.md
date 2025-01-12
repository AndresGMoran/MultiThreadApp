**Proyecto final 1º trimestre - Andrés Moran - Video explicativo** https://youtu.be/r6a2wTOa6aI

### 1. **Juego (Game)**
- **Funcionalidad:** Implementa un juego en el que los círculos aparecen aleatoriamente en un lienzo, y el jugador debe hacer clic en ellos para ganar puntos.
- **Uso de hilos:**
    - **Generación de círculos:** Utiliza un hilo para generar círculos de forma aleatoria cada cierto intervalo.
    - **Lógica del juego:** Otro hilo ejecuta el bucle principal, actualizando el lienzo y controlando el flujo del juego.

### 2. **Administrador de Tareas**
- **Funcionalidad:** Muestra una lista actualizada de procesos del sistema con información sobre uso de CPU, memoria y PID.
- **Uso de hilos:**
  - El método (start_updating_processes) inicia un hilo para actualizar la lista de procesos cada 5 segundos.

### 3. **Gráficos Criptomonedas e IBEX**
- **Funcionalidad:** Muestra gráficos de datos financieros, actualizados periódicamente desde APIs externas.
- **Uso de hilos:**
  - Dos hilos (uno para criptomonedas y otro para IBEX) se encargan de consultar datos y actualizar los gráficos cada minuto.

### 4. **Monitorización del Sistema**
- **Funcionalidad:** Monitoriza y muestra en tiempo real el uso de CPU, RAM, estado de la batería y actividad de red.
- **Uso de hilos:**
  - Cada monitorización tiene su propio hilo que consulta periódicamente información del sistema y actualiza los elementos de la interfaz.

### 5. **Panel Derecho (Chat y Música)**
- **Funcionalidad:** Incluye un chat sencillo y un reproductor de música.
- **Uso de hilos:**
  - **Chat:** Al enviar un mensaje, se utiliza un hilo para evitar retrasos mientras se actualiza la lista de mensajes.
  - **Reproductor de música:** Cada acción (“Play”, “Pause”, “Restart”) se ejecuta en hilos separados, asegurando una respuesta rápida.

### 6. **Panel Izquierdo (Clima y Noticias)**
- **Funcionalidad:** Muestra información del clima y noticias en tiempo real.
- **Uso de hilos:**
  - **Clima:** Se utiliza un hilo para consultar la API de OpenWeather y actualizar el clima.
  - **Noticias:** Otro hilo consulta una API de noticias y actualiza el panel.

### 7. **Pomodoro**
- **Funcionalidad:** Implementa un temporizador Pomodoro con opciones para configurar tiempos de trabajo y descanso.
- **Uso de hilos:**
  - El método (start_timer) inicia un hilo para gestionar la cuenta atras del temporizador.
  - La interfaz permanece responsive incluso mientras el temporizador está en marcha.

### 8. **Scraping**
- **Funcionalidad:** Realiza scraping en un sitio web, extrae enlaces y los guarda en una base de datos.
- **Uso de hilos:**
  - **Scraping:** Un hilo se encarga de extraer los enlaces del sitio web.
  - **Inserción:** Otro hilo almacena los enlaces extraídos en la base de datos.

### 9. **Lista de Tareas (To-Do List)**
- **Funcionalidad:** Permite gestionar una lista de tareas con opciones para agregar, eliminar y marcar tareas como completadas.
- **Uso de hilos:**
  - Cada acción (“Agregar”, “Eliminar”, “Marcar como completada”) se ejecuta en un hilo independiente.

