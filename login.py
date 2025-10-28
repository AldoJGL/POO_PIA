import tkinter as tk
from tkinter import messagebox, simpledialog
from conn import conectar
import hashlib

def verificar_contrasena(contrasena_ingresada, contrasena_guardada):
    return hashlib.sha256(contrasena_ingresada.encode()).hexdigest() == contrasena_guardada

def login():
    conexion = conectar()
    cursor = conexion.cursor()

    ventana = tk.Tk()
    ventana.title("Iniciar sesion - Taller de computacion")
    ventana.geometry("900x600")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=300)
    navbar.pack(fill="x")
    titulo = tk.Label(navbar,
                      text="Taller de computacion",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 20, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    frame_login = tk.Frame(ventana, bg="#E0E0E0")
    frame_login.pack(expand=True)

    tk.Label(frame_login, text="Correo universitario:", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=10, sticky="e")
    entry_correo = tk.Entry(frame_login, bg="white", fg="black", highlightthickness=1, highlightbackground="black", width=35)
    entry_correo.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(frame_login, text="Contraseña:", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=1, column=0, pady=10, sticky="e")
    entry_contrasena = tk.Entry(frame_login, bg="white", fg="black", highlightthickness=1, highlightbackground="black", width=35, show="*")
    entry_contrasena.grid(row=1, column=1, pady=10, padx=10)

    def validar_login():
        correo = entry_correo.get()
        contrasena = entry_contrasena.get()

        if not correo or not contrasena:
            messagebox.showwarning("Campos vacios", "Por favor completa todos los campos.")
            return

        cursor.execute("""
            SELECT id_usuario, contrasena_us, nombre_usuario, rol
            FROM usuarios
            WHERE correo_usuario = ?
        """, (correo,))
        resultado = cursor.fetchone()

        if resultado:
            id_usuario, contrasena_guardada, nombre, rol = resultado
            if verificar_contrasena(contrasena, contrasena_guardada):
                conexion.close()
                ventana.destroy()
                if rol.lower() == "administrador":
                    from menu_admin import menu_admin
                    menu_admin(nombre, rol, id_usuario)
                else:
                    from menu import menu_alumno
                    menu_alumno(nombre, id_usuario)
                return
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
                return

        cursor.execute("""
            SELECT id_alumno, contrasena, nombre_alumno
            FROM alumnos
            WHERE correo = ?
        """, (correo,))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            id_alumno, contrasena_guardada, nombre = resultado
            if verificar_contrasena(contrasena, contrasena_guardada):
                ventana.destroy()
                from menu import mostrar_menu
                mostrar_menu(nombre, id_alumno)
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "No existe ese usuario registrado")

    boton_login = tk.Button(frame_login,
                            text="Iniciar sesion",
                            bg="#1A3E5C",
                            fg="white",
                            font=("Arial", 12, "bold"),
                            relief="flat",
                            width=20,
                            height=2,
                            command=validar_login)
    boton_login.grid(row=3, column=0, columnspan=2, pady=20)

    ventana.mainloop()

