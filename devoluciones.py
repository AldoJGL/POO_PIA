import tkinter as tk
from tkinter import messagebox, ttk
from conn import conectar
import sqlite3

def devolver_equipo(menu_admin=None):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT p.id_prestamo, a.nombre_alumno, e.nombre_equipo, e.serie_equipo, e.estado
        FROM prestamos p
        JOIN alumnos a ON p.id_alumno = a.id_alumno
        JOIN equipos e ON p.id_equipo = e.id_equipo
        WHERE p.devuelto = 'No'
    """)
    prestamos = cursor.fetchall()

    if not prestamos:
        messagebox.showinfo("Sin prestamos", "No hay prestamos activos.")
        conexion.close()
        return

    ventana = tk.Tk()
    ventana.title("Devoluciones - Taller de Computacion")
    ventana.geometry("800x500")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=80)
    navbar.pack(fill="x")
    titulo = tk.Label(navbar,
                      text="Devoluciones de equipos",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 18, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    frame_contenido = tk.Frame(ventana, bg="#E0E0E0")
    frame_contenido.pack(expand=True, pady=20)

    columnas = ("No.", "Alumno", "Equipo", "Serie", "Estado")
    tree = ttk.Treeview(frame_contenido, columns=columnas, show="headings", height=10)
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack(pady=20)

    for idx, pre in enumerate(prestamos, start=1):
        id_pre, nombre_alumno, nombre_equipo, serie, estado = pre
        tree.insert("", tk.END, values=(idx, nombre_alumno, nombre_equipo, serie, estado))

    def marcar_devuelto():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Seleccion vacia", "Selecciona un prestamo de la lista.")
            return

        idx = int(tree.item(seleccion[0])["values"][0]) - 1
        id_prestamo, nombre_alumno, nombre_equipo, serie, estado = prestamos[idx]

        cursor.execute("SELECT id_equipo, id_alumno FROM prestamos WHERE id_prestamo = ?", (id_prestamo,))
        resultado = cursor.fetchone()
        id_equipo, id_alumno = resultado

        try:
            cursor.execute("""
                UPDATE prestamos
                SET devuelto = 'Si', fecha_devolucion = CURRENT_TIMESTAMP
                WHERE id_prestamo = ?
            """, (id_prestamo,))

            cursor.execute("""
                UPDATE equipos
                SET estado = 'Disponible'
                WHERE id_equipo = ?
            """, (id_equipo,))

            cursor.execute("""
                UPDATE horarios
                SET fecha_devolucion = CURRENT_TIMESTAMP
                WHERE id_equipo = ? AND id_alumno = ? AND fecha_devolucion IS NULL
            """, (id_equipo, id_alumno))

            conexion.commit()
            messagebox.showinfo("Éxito", f"Devolucoon registrada para '{nombre_equipo}' del alumno '{nombre_alumno}'.")
            tree.delete(seleccion[0])
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo procesar la devolucion:\n{e}")

    frame_botones = tk.Frame(frame_contenido, bg="#E0E0E0")
    frame_botones.pack(pady=10)

    boton_devolver = tk.Button(frame_botones,
                               text="Marcar como devuelto",
                               bg="#1A3E5C",
                               fg="white",
                               font=("Arial", 12, "bold"),
                               relief="flat",
                               width=20,
                               height=2,
                               command=marcar_devuelto)
    boton_devolver.grid(row=0, column=0, padx=5)

    def regresar():
        ventana.destroy()
        if menu_admin:
            menu_admin()

    boton_regresar = tk.Button(frame_botones,
                               text="Regresar",
                               bg="#1A3E5C",
                               fg="white",
                               font=("Arial", 12, "bold"),
                               relief="flat",
                               width=20,
                               height=2,
                               command=regresar)
    boton_regresar.grid(row=0, column=1, padx=5)

    ventana.mainloop()
    conexion.close()

