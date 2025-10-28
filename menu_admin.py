import tkinter as tk
from tkinter import messagebox
from devoluciones import devolver_equipo
from consultar import consultar_equipos
from agregar_equipos import agregar_equipo
from historial_prestamos import historial_prestamos
from conn import conectar
import hashlib

def registrar_empleado():
    conexion = conectar()
    cursor = conexion.cursor()

    nombre = tk.simpledialog.askstring("Nombre", "Nombre del empleado:")
    correo = tk.simpledialog.askstring("Correo", "Correo del empleado:")
    contrasena = tk.simpledialog.askstring("Contraseña", "Contraseña:", show="*")
    rol = tk.simpledialog.askstring("Rol", "Rol (empleado/administrador):").lower()

    if rol not in ["empleado", "administrador"]:
        messagebox.showerror("Error", "Rol invalido. Debe ser 'empleado' o 'administrador'.")
        conexion.close()
        return

    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

    try:
        cursor.execute("""
            INSERT INTO usuarios(nombre_usuario, rol, correo_usuario, contrasena_us)
            VALUES (?, ?, ?, ?)
        """, (nombre, rol, correo, contrasena_hash))
        conexion.commit()
        messagebox.showinfo(f"Empleado '{nombre}' registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar empleado: {e}")
    finally:
        conexion.close()


def menu_admin(nombre, rol, id_usuario):
    ventana = tk.Tk()
    ventana.title(f"Menu Administrador - {nombre} ({rol})")
    ventana.geometry("900x600")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=300)
    navbar.pack(fill="x")

    titulo = tk.Label(navbar,
                      text=f"Menú Admin - {nombre} ({rol})",
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

    def accion_devolver():
        devolver_equipo()

    def accion_consultar():
        consultar_equipos()

    def accion_registrar_empleado():
        registrar_empleado()

    def accion_agregar_equipo():
        agregar_equipo()

    def accion_ver_historial():
        historial_prestamos()

    def accion_salir():
        if messagebox.askyesno("Cerrar sesion", "¿Seguro que quieres cerrar sesion?"):
            ventana.destroy()

    boton1 = boton_estilo("Registrar devolucion", accion_devolver)
    boton1.pack(pady=10)

    boton2 = boton_estilo("Consultar equipos", accion_consultar)
    boton2.pack(pady=10)

    boton3 = boton_estilo("Agregar empleado", accion_registrar_empleado)
    boton3.pack(pady=10)

    boton4 = boton_estilo("Agregar equipo", accion_agregar_equipo)
    boton4.pack(pady=10)

    boton5 = boton_estilo("Ver historial de prestamos", accion_ver_historial)
    boton5.pack(pady=10)

    boton6 = boton_estilo("Salir", accion_salir)
    boton6.pack(pady=10)

    ventana.mainloop()
