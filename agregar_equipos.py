import tkinter as tk
from tkinter import messagebox
from conn import conectar
import sqlite3

def agregar_equipo(menu_admin=None):
    ventana = tk.Tk()
    ventana.title("Agregar Equipo - Taller de Computacion")
    ventana.geometry("600x500")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=80)
    navbar.pack(fill="x")
    titulo = tk.Label(navbar,
                      text="Registrar nuevo equipo",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 18, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    frame_form = tk.Frame(ventana, bg="#E0E0E0")
    frame_form.pack(pady=30)

    tk.Label(frame_form, text="Nombre del equipo:", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    entry_nombre = tk.Entry(frame_form, width=35, bg="white", fg="black", highlightthickness=1, highlightbackground="black")
    entry_nombre.grid(row=0, column=1, pady=5)

    tk.Label(frame_form, text="Número/Serie del equipo:", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    entry_serie = tk.Entry(frame_form, width=35, bg="white", fg="black", highlightthickness=1, highlightbackground="black")
    entry_serie.grid(row=1, column=1, pady=5)

    tk.Label(frame_form, text="Estado:", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    entry_estado = tk.Entry(frame_form, width=35, bg="white", fg="black", highlightthickness=1, highlightbackground="black")
    entry_estado.grid(row=2, column=1, pady=5)
    entry_estado.insert(0, "Disponible")

    tk.Label(frame_form, text="Descripcion:", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="e", pady=5, padx=5)
    entry_desc = tk.Entry(frame_form, width=35, bg="white", fg="black", highlightthickness=1, highlightbackground="black")
    entry_desc.grid(row=3, column=1, pady=5)

    def guardar_equipo():
        nombre_equipo = entry_nombre.get().strip()
        serie_equipo = entry_serie.get().strip()
        estado = entry_estado.get().strip()
        if not estado:
            estado = "Disponible"
        descripcion = entry_desc.get().strip()

        if not nombre_equipo or not serie_equipo:
            messagebox.showwarning("Campos vacios", "Nombre y serie del equipo son obligatorios.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO equipos (nombre_equipo, serie_equipo, estado, descripcion)
                VALUES (?, ?, ?, ?)
            """, (nombre_equipo, serie_equipo, estado, descripcion))
            conexion.commit()
            messagebox.showinfo("Registrado", "Equipo registrado correctamente.")
            entry_nombre.delete(0, tk.END)
            entry_serie.delete(0, tk.END)
            entry_estado.delete(0, tk.END)
            entry_estado.insert(0, "Disponible")
            entry_desc.delete(0, tk.END)
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error en el numero de serie: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar el equipo: {e}")
        finally:
            conexion.close()

    frame_botones = tk.Frame(ventana, bg="#E0E0E0")
    frame_botones.pack(pady=20)

    boton_guardar = tk.Button(frame_botones,
                              text="Agregar equipo",
                              bg="#1A3E5C",
                              fg="white",
                              font=("Arial", 12, "bold"),
                              relief="flat",
                              width=15,
                              height=2,
                              command=guardar_equipo)
    boton_guardar.grid(row=0, column=0, padx=5)

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
                               width=15,
                               height=2,
                               command=regresar)
    boton_regresar.grid(row=0, column=1, padx=5)

    ventana.mainloop()
