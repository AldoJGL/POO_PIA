import tkinter as tk
from tkinter import ttk
from conn import conectar
import sqlite3

def historial_prestamos(menu_admin=None):
    conexion = conectar()
    cursor = conexion.cursor()

    ventana = tk.Tk()
    ventana.title("Historial de prestamos - Administrador")
    ventana.geometry("900x500")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=80)
    navbar.pack(fill="x")
    titulo = tk.Label(navbar,
                      text="Historial de prestamos y devoluciones",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 18, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    frame_contenido = tk.Frame(ventana, bg="#E0E0E0")
    frame_contenido.pack(expand=True, pady=20)

    columnas = ("Alumno", "Equipo", "Serie", "Fecha Prestamo", "Fecha Devolucion")
    tree = ttk.Treeview(frame_contenido, columns=columnas, show="headings", height=15)
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=160, anchor="center")
    tree.pack(pady=20)

    cursor.execute("""
        SELECT a.nombre_alumno, e.nombre_equipo, e.serie_equipo,
               h.fecha_prestamo, IFNULL(h.fecha_devolucion, 'No devuelto')
        FROM horarios h
        JOIN alumnos a ON h.id_alumno = a.id_alumno
        JOIN equipos e ON h.id_equipo = e.id_equipo
        ORDER BY h.fecha_prestamo DESC
    """)
    registros = cursor.fetchall()

    for registro in registros:
        tree.insert("", tk.END, values=registro)

    def regresar():
        ventana.destroy()
        if menu_admin:
            menu_admin()

    boton_regresar = tk.Button(frame_contenido,
                               text="Regresar",
                               bg="#1A3E5C",
                               fg="white",
                               font=("Arial", 12, "bold"),
                               relief="flat",
                               width=20,
                               height=2,
                               command=regresar)
    boton_regresar.pack(pady=10)

    ventana.mainloop()
    conexion.close()
