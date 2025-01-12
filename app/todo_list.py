import tkinter as tk
import threading
import time

def actualizar_todo_list(todo_listbox, tareas):
    """Actualizar el contenido del ListBox con las tareas actuales."""
    todo_listbox.delete(0, tk.END)
    for tarea, completada in tareas:
        estado = "[X]" if completada else "[ ]"
        todo_listbox.insert(tk.END, f"{estado} {tarea}")

def agregar_tarea(entry, todo_listbox, tareas):
    """Agregar una nueva tarea a la lista en un hilo separado."""
    def tarea_hilo():
        nueva_tarea = entry.get()
        if nueva_tarea.strip():
            tareas.append((nueva_tarea, False))  # Agregar tarea como no completada
            todo_listbox.after(0, actualizar_todo_list, todo_listbox, tareas)
        entry.delete(0, tk.END)
    threading.Thread(target=tarea_hilo).start()

def eliminar_tarea(todo_listbox, tareas):
    """Eliminar la tarea seleccionada de la lista en un hilo separado."""
    def tarea_hilo():
        seleccion = todo_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            tareas.pop(indice)
            todo_listbox.after(0, actualizar_todo_list, todo_listbox, tareas)
    threading.Thread(target=tarea_hilo).start()

def marcar_tarea(todo_listbox, tareas):
    """Marcar la tarea seleccionada como completada o no completada en un hilo separado."""
    def tarea_hilo():
        seleccion = todo_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            tarea, completada = tareas[indice]
            tareas[indice] = (tarea, not completada)  # Alternar el estado de completada
            todo_listbox.after(0, actualizar_todo_list, todo_listbox, tareas)
    threading.Thread(target=tarea_hilo).start()

def crear_solapa_todo(tab):
    """Función para inicializar la funcionalidad de la lista To-Do en la solapa."""
    tareas = []

    # Entrada para agregar nuevas tareas
    entry = tk.Entry(tab, font=("Arial", 12))
    entry.pack(pady=10, padx=10, fill="x")

    # Botón para agregar tareas
    boton_agregar = tk.Button(tab, text="Agregar", command=lambda: agregar_tarea(entry, todo_listbox, tareas))
    boton_agregar.pack(pady=5)

    # ListBox para mostrar las tareas
    todo_listbox = tk.Listbox(tab, font=("Arial", 12), height=10)
    todo_listbox.pack(pady=10, padx=10, fill="both", expand=True)

    # Botón para eliminar tareas
    boton_eliminar = tk.Button(tab, text="Eliminar", command=lambda: eliminar_tarea(todo_listbox, tareas))
    boton_eliminar.pack(pady=5)

    # Botón para marcar tareas como completadas o no completadas
    boton_marcar = tk.Button(tab, text="Marcar como hecho/no hecho", command=lambda: marcar_tarea(todo_listbox, tareas))
    boton_marcar.pack(pady=5)

    # Inicializar la lista vacía
    actualizar_todo_list(todo_listbox, tareas)
