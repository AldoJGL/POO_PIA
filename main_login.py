import tkinter as tk
from tkinter import messagebox
from login import login
from registro import registrar_alumno
from main import main

def menu_principal():
    ventana = tk.Tk()
    ventana.title("Sistema de Prestamos de Equipos")
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

    frame_contenido = tk.Frame(ventana, bg="#E0E0E0")
    frame_contenido.pack(expand=True, pady=80)

    def boton_estilo(texto, comando):
        return tk.Button(frame_contenido,
                         text=texto,
                         bg="#1A3E5C",
                         fg="white",
                         font=("Arial", 12, "bold"),
                         relief="flat",
                         width=25,
                         height=2,
                         command=comando)

    def iniciar_sesion():
        ventana.destroy()
        usuario_sesion = login()
        if usuario_sesion:
            messagebox.showinfo("Inicio de sesion", f"Sesion iniciada correctamente: {usuario_sesion['nombre']} ({usuario_sesion['rol']})")
            main(usuario_sesion)

    def registrarse():
        ventana.destroy()
        usuario_sesion = registrar_alumno()
        if usuario_sesion:
            messagebox.showinfo("Registro", f"Registro y sesion iniciados correctamente: {usuario_sesion['nombre']} ({usuario_sesion['rol']})")
            main(usuario_sesion)

    def salir():
        if messagebox.askyesno("Salir", "¿Seguro que quieres salir del sistema?"):
            ventana.destroy()

    boton_iniciar = boton_estilo("Iniciar sesion", iniciar_sesion)
    boton_iniciar.pack(pady=15)

    boton_registro = boton_estilo("Registrarse", registrarse)
    boton_registro.pack(pady=15)

    boton_salir = boton_estilo("Salir", salir)
    boton_salir.pack(pady=15)

    ventana.mainloop()


if __name__ == "__main__":
    menu_principal()
