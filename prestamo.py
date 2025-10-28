import tkinter as tk
from tkinter import messagebox, ttk
from conn import conectar
import sqlite3

def pedir_prestamo(id_alumno, menu_anterior=None):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_equipo, nombre_equipo, serie_equipo, estado 
        FROM equipos 
        WHERE estado = 'Disponible'
    """)
    equipos = cursor.fetchall()

    if not equipos:
        messagebox.showinfo("No hay equipos", "No hay equipos disponibles para prestamo.")
        conexion.close()
        return

    ventana = tk.Tk()
    ventana.title("Pedir prestamo - Taller de Computacioon")
    ventana.geometry("800x500")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=80)
    navbar.pack(fill="x")
    titulo = tk.Label(navbar,
                      text="Equipos disponibles para prestamo",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 18, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    frame_contenido = tk.Frame(ventana, bg="#E0E0E0")
    frame_contenido.pack(expand=True, pady=20)

    columnas = ("ID", "Nombre", "Serie", "Estado")
    tree = ttk.Treeview(frame_contenido, columns=columnas, show="headings", height=10)
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack(pady=20)

    for eq in equipos:
        tree.insert("", tk.END, values=eq)

    def solicitar_prestamo():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("No se selecciono", "Selecciona un equipo de la lista.")
            return
        id_equipo = tree.item(seleccion[0])["values"][0]

        cursor.execute("SELECT estado FROM equipos WHERE id_equipo = ?", (id_equipo,))
        resultado = cursor.fetchone()
        if not resultado:
            messagebox.showerror("Error", "No existe ese equipo.")
            return

        if resultado[0] != "Disponible":
            messagebox.showerror("No disponible", "El equipo no esta disponible.")
            return

        try:
            cursor.execute("""
                INSERT INTO prestamos (id_equipo, id_alumno, devuelto)
                VALUES (?, ?, 'No')
            """, (id_equipo, id_alumno))
            conexion.commit()

            cursor.execute("""
                INSERT INTO horarios (id_equipo, id_alumno, fecha_prestamo)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (id_equipo, id_alumno))

            cursor.execute("UPDATE equipos SET estado = 'Prestado' WHERE id_equipo = ?", (id_equipo,))
            conexion.commit()

            messagebox.showinfo("Registrado", "Prestamo registrado correctamente y horario actualizado.")
            ventana.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el prestamo:\n{e}")
        finally:
            conexion.close()

    frame_botones = tk.Frame(frame_contenido, bg="#E0E0E0")
    frame_botones.pack(pady=10)

    boton_prestamo = tk.Button(frame_botones,
                               text="Pedir prestamo",
                               bg="#1A3E5C",
                               fg="white",
                               font=("Arial", 12, "bold"),
                               relief="flat",
                               width=20,
                               height=2,
                               command=solicitar_prestamo)
    boton_prestamo.grid(row=0, column=0, padx=5)

    def regresar():
        ventana.destroy()
        if menu_anterior:
            menu_anterior()

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

