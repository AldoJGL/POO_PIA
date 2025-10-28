import tkinter as tk
from tkinter import messagebox
from conn import conectar
import hashlib
import re
from login import login

def hash_contrasena(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validar_correo(correo):
    patron = r"^[\w\.-]+@uanl\.edu\.mx$"
    return re.match(patron, correo) is not None

def registrar_alumno():
    ventana = tk.Tk()
    ventana.title("Registrar Alumno - Taller de Computación")
    ventana.geometry("900x600")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=300)
    navbar.pack(fill="x")
    titulo = tk.Label(navbar,
                      text="Registrar nuevo alumno",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 20, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    frame_registro = tk.Frame(ventana, bg="#E0E0E0")
    frame_registro.pack(expand=True)

    tk.Label(frame_registro, text="Nombre completo:", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=10, sticky="e")
    entry_nombre = tk.Entry(frame_registro, bg="white", fg="black", highlightthickness=1, highlightbackground="black", width=35)
    entry_nombre.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(frame_registro, text="Correo universitario (@uanl.edu.mx):", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=1, column=0, pady=10, sticky="e")
    entry_correo = tk.Entry(frame_registro, bg="white", fg="black", highlightthickness=1, highlightbackground="black", width=35)
    entry_correo.grid(row=1, column=1, pady=10, padx=10)

    tk.Label(frame_registro, text="Contraseña:", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=2, column=0, pady=10, sticky="e")
    entry_contrasena = tk.Entry(frame_registro, bg="white", fg="black", highlightthickness=1, highlightbackground="black", width=35, show="*")
    entry_contrasena.grid(row=2, column=1, pady=10, padx=10)

    # ===== Función de registro =====
    def registrar():
        nombre = entry_nombre.get()
        correo = entry_correo.get()
        contrasena = entry_contrasena.get()

        if not nombre or not correo or not contrasena:
            messagebox.showwarning("Campos vacios", "Por fvor completa todos los campos")
            return

        if not validar_correo(correo):
            messagebox.showerror("Correo invalido", "El correo debe terminar con @uanl.edu.mx")
            return

        contrasena_hash = hash_contrasena(contrasena)
        conexion = conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO alumnos (nombre_alumno, correo, contrasena)
                VALUES (?, ?, ?)
            """, (nombre, correo, contrasena_hash))
            conexion.commit()
            messagebox.showinfo("Éxito", f"Alumno '{nombre}' registrado correctamente.")
            ventana.destroy()
            login()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el alumno:\n{e}")
        finally:
            conexion.close()

    boton_registrar = tk.Button(frame_registro,
                                text="Registrar",
                                bg="#1A3E5C",
                                fg="white",
                                font=("Arial", 12, "bold"),
                                relief="flat",
                                width=20,
                                height=2,
                                command=registrar)
    boton_registrar.grid(row=3, column=0, columnspan=2, pady=20)

    ventana.mainloop()


if __name__ == "__main__":
    registrar_alumno()

