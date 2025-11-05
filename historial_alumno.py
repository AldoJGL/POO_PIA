import tkinter as tk
from tkinter import ttk, messagebox
from conn import conectar
import sqlite3

def historial_alumno(id_alumno, menu_alumno=None):
    conexion = conectar()
    cursor = conexion.cursor()

    ventana = tk.Tk()
    ventana.title("Historial de préstamos - Alumno")
    ventana.geometry("900x500")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    # ===== Navbar =====
    navbar = tk.Frame(ventana, bg="#1A3E5C", height=80)
    navbar.pack(fill="x")
    titulo = tk.Label(navbar,
                      text="Historial de tus préstamos",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 18, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    # ===== Frame de contenido =====
    frame_contenido = tk.Frame(ventana, bg="#E0E0E0")
    frame_contenido.pack(expand=True, pady=20)

    # ===== Treeview =====
    columnas = ("Equipo", "Serie", "Fecha Préstamo", "Fecha Devolución")
    tree = ttk.Treeview(frame_contenido, columns=columnas, show="headings", height=15)
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")
    tree.pack(pady=20)

    # ===== Consultar historial del alumno =====
    try:
        cursor.execute("""
            SELECT e.nombre_equipo, e.serie_equipo,
                   h.fecha_prestamo, IFNULL(h.fecha_devolucion, 'No devuelto')
            FROM horarios h
            JOIN equipos e ON h.id_equipo = e.id_equipo
            WHERE h.id_alumno = ?
            ORDER BY h.fecha_prestamo DESC
        """, (id_alumno,))
        registros = cursor.fetchall()

        if not registros:
            messagebox.showinfo("Sin historial", "Aún no has realizado ningún préstamo.")
        else:
            for registro in registros:
                tree.insert("", tk.END, values=registro)

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener el historial:\n{e}")

    # ===== Botón Regresar =====
    def regresar():
        ventana.destroy()
        if menu_alumno:
            menu_alumno()

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
