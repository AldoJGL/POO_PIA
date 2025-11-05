import tkinter as tk
from tkinter import messagebox
from consultar import consultar_equipos
from prestamo import pedir_prestamo
from historial_alumno import historial_alumno

def mostrar_menu(nombre, id_alumno):
    ventana = tk.Tk()
    ventana.title(f"Menu Principal - {nombre}")
    ventana.geometry("900x600")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=300)
    navbar.pack(fill="x")

    titulo = tk.Label(navbar,
                      text=f"Menu Principal - {nombre}",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 20, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    frame_contenido = tk.Frame(ventana, bg="#E0E0E0")
    frame_contenido.pack(expand=True, pady=80)

    def boton_estilo(texto, comando):
        return tk.Button(frame_contenido,
                         text=texto,
                         bg="#1A3E5C",
                         fg="white",
                         font=("Arial", 12, "bold"),
                         relief="flat",
                         width=30,
                         height=2,
                         command=comando)

    def accion_consultar():
        consultar_equipos()

    def accion_prestamo():
        pedir_prestamo(id_alumno)

    def accion_historial():
        ventana.destroy()
        historial_alumno(id_alumno, lambda: mostrar_menu(nombre, id_alumno))

    def accion_cerrar():
        if messagebox.askyesno("Cerrar sesion", "¿Seguro que quieres cerrar sesion?"):
            ventana.destroy()

    boton1 = boton_estilo("Consultar equipos disponibles", accion_consultar)
    boton1.pack(pady=10)

    boton2 = boton_estilo("Pedir prestamo de equipo", accion_prestamo)
    boton2.pack(pady=10)

    boton3 = boton_estilo("Ver historial de prestamos", accion_historial)
    boton3.pack(pady=10)

    boton4 = boton_estilo("Cerrar sesion", accion_cerrar)
    boton4.pack(pady=10)

    ventana.mainloop()
