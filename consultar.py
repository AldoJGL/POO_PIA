import tkinter as tk
from tkinter import ttk, messagebox
from conn import conectar

def consultar_equipos(menu_anterior=None):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_equipo, nombre_equipo, serie_equipo, estado, descripcion FROM equipos")
    equipos = cursor.fetchall()

    if not equipos:
        messagebox.showinfo("Informacion", "No hay equipos registrados.")
        conexion.close()
        return

    ventana = tk.Tk()
    ventana.title("Consultar Equipos - Taller de Computacion")
    ventana.geometry("950x500")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=80)
    navbar.pack(fill="x")
    titulo = tk.Label(navbar,
                      text="Todos los equipos registrados",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 18, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    frame_principal = tk.Frame(ventana, bg="#E0E0E0")
    frame_principal.pack(expand=True, fill="both", pady=10)

    columnas = ("ID", "Nombre", "Serie", "Estado", "Descripcion")
    frame_tabla = tk.Frame(frame_principal, bg="#E0E0E0")
    frame_tabla.pack(fill="both", expand=True, pady=10)

    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack(fill="both", expand=True)

    for eq in equipos:
        tree.insert("", tk.END, values=eq)

    frame_botones = tk.Frame(frame_principal, bg="#E0E0E0")
    frame_botones.pack(pady=10)

    tk.Label(frame_botones, text="Buscar por nombre:", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
    entry_buscar = tk.Entry(frame_botones, width=35, bg="white", fg="black", highlightthickness=1, highlightbackground="black")
    entry_buscar.grid(row=0, column=1, padx=5)

    def buscar():
        busqueda = entry_buscar.get().strip()
        for item in tree.get_children():
            tree.delete(item)

        if busqueda == "":
            for eq in equipos:
                tree.insert("", tk.END, values=eq)
            return

        cursor.execute("""
            SELECT id_equipo, nombre_equipo, serie_equipo, estado, descripcion
            FROM equipos
            WHERE nombre_equipo LIKE ?
        """, ('%' + busqueda + '%',))
        resultados = cursor.fetchall()

        if resultados:
            for eq in resultados:
                tree.insert("", tk.END, values=eq)
        else:
            messagebox.showinfo("No encontrado", f"No se encontraron equipos con '{busqueda}'.")

    def regresar():
        ventana.destroy()
        if menu_anterior:
            menu_anterior()

    boton_buscar = tk.Button(frame_botones,
                             text="Buscar",
                             bg="#1A3E5C",
                             fg="white",
                             font=("Arial", 12, "bold"),
                             relief="flat",
                             width=15,
                             height=2,
                             command=buscar)
    boton_buscar.grid(row=0, column=2, padx=5)

    boton_regresar = tk.Button(frame_botones,
                               text="Regresar",
                               bg="#1A3E5C",
                               fg="white",
                               font=("Arial", 12, "bold"),
                               relief="flat",
                               width=15,
                               height=2,
                               command=regresar)
    boton_regresar.grid(row=0, column=3, padx=5)

    ventana.mainloop()
    conexion.close()
