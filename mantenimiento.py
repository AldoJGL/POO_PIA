import tkinter as tk
from tkinter import ttk, messagebox
from conn import conectar
import sqlite3

def mantenimiento(id_usuario):
    conexion = conectar()
    cursor = conexion.cursor()

    ventana = tk.Tk()
    ventana.title("Registro de Mantenimiento - Taller de Computacion")
    ventana.geometry("950x600")
    ventana.configure(bg="#E0E0E0")
    ventana.resizable(False, False)

    navbar = tk.Frame(ventana, bg="#1A3E5C", height=80)
    navbar.pack(fill="x")

    titulo = tk.Label(navbar,
                      text="Registro y Control de Mantenimiento",
                      bg="#1A3E5C",
                      fg="white",
                      font=("Arial", 18, "bold"),
                      anchor="w",
                      padx=20)
    titulo.pack(fill="both", expand=True)

    frame_principal = tk.Frame(ventana, bg="#E0E0E0", padx=20, pady=20)
    frame_principal.pack(fill="both", expand=True)

    cursor.execute("SELECT id_equipo, nombre_equipo FROM equipos")
    equipos = cursor.fetchall()

    tk.Label(frame_principal, text="Equipo:", bg="#E0E0E0", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    combo_equipo = ttk.Combobox(frame_principal, values=[f"{e[0]} - {e[1]}" for e in equipos], width=40, state="readonly")
    combo_equipo.grid(row=0, column=1, pady=5)

    tk.Label(frame_principal, text="Tipo de mantenimiento:", bg="#E0E0E0", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_tipo = tk.Entry(frame_principal, width=45)
    entry_tipo.grid(row=1, column=1, pady=5)

    tk.Label(frame_principal, text="Descripción:", bg="#E0E0E0", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_desc = tk.Entry(frame_principal, width=45)
    entry_desc.grid(row=2, column=1, pady=5)

    tk.Label(frame_principal, text="Costo ($):", bg="#E0E0E0", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_costo = tk.Entry(frame_principal, width=20)
    entry_costo.grid(row=3, column=1, sticky="w", pady=5)

    def registrar_mantenimiento():
        seleccion = combo_equipo.get()
        if not seleccion:
            messagebox.showwarning("Error", "Selecciona un equipo.")
            return

        id_equipo = int(seleccion.split(" - ")[0])
        tipo = entry_tipo.get().strip()
        desc = entry_desc.get().strip()
        costo = entry_costo.get().strip()

        if not tipo or not costo:
            messagebox.showwarning("Campos vacios", "El tipo y el costo son obligatorios.")
            return

        try:
            costo_val = float(costo)
        except ValueError:
            messagebox.showwarning("Error", "El costo debe ser un número valido.")
            return

        try:
            cursor.execute("""
                INSERT INTO mantenimiento (id_equipo, tipo_mantenimiento, descripcion, costo_mantenimiento, id_usuario)
                VALUES (?, ?, ?, ?, ?)
            """, (id_equipo, tipo, desc, costo_val, id_usuario))

            cursor.execute("UPDATE equipos SET estado = 'En mantenimiento' WHERE id_equipo = ?", (id_equipo,))
            conexion.commit()

            messagebox.showinfo("Éxito", "Mantenimiento registrado correctamente.")
            actualizar_tabla()

            entry_tipo.delete(0, tk.END)
            entry_desc.delete(0, tk.END)
            entry_costo.delete(0, tk.END)
            combo_equipo.set("")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el mantenimiento:\n{e}")

    columnas = ("ID", "Equipo", "Tipo", "Descripcion", "Fecha", "Costo", "Registrado por")
    tree = ttk.Treeview(frame_principal, columns=columnas, show="headings", height=10)
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.grid(row=5, column=0, columnspan=3, pady=20)

    def actualizar_tabla():
        for row in tree.get_children():
            tree.delete(row)

        cursor.execute("""
            SELECT m.id_mantenimiento, e.nombre_equipo, m.tipo_mantenimiento, m.descripcion,
                   m.fecha_mantenimiento, m.costo_mantenimiento, u.nombre_usuario
            FROM mantenimiento m
            JOIN equipos e ON m.id_equipo = e.id_equipo
            JOIN usuarios u ON m.id_usuario = u.id_usuario
            ORDER BY m.fecha_mantenimiento DESC
        """)
        for fila in cursor.fetchall():
            tree.insert("", tk.END, values=fila)

    actualizar_tabla()

    frame_botones = tk.Frame(frame_principal, bg="#E0E0E0")
    frame_botones.grid(row=4, column=0, columnspan=3, pady=10)

    tk.Button(frame_botones, text="Registrar mantenimiento", bg="#1A3E5C", fg="white",
              font=("Arial", 11, "bold"), width=22, relief="flat",
              command=registrar_mantenimiento).pack(side="left", padx=10)

    tk.Button(frame_botones, text="Actualizar lista", bg="#4CAF50", fg="white",
              font=("Arial", 11, "bold"), width=18, relief="flat",
              command=actualizar_tabla).pack(side="left", padx=10)

    def marcar_disponible():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un registro en la tabla.")
            return

        valores = tree.item(seleccionado, "values")
        nombre_equipo = valores[1]

        cursor.execute("SELECT id_equipo FROM equipos WHERE nombre_equipo = ?", (nombre_equipo,))
        equipo = cursor.fetchone()
        if not equipo:
            messagebox.showerror("Error", "No se encontro el equipo en la base de datos.")
            return
        id_equipo = equipo[0]

        try:
            cursor.execute("UPDATE equipos SET estado = 'Disponible' WHERE id_equipo = ?", (id_equipo,))
            conexion.commit()
            messagebox.showinfo("Éxito", f"El equipo '{nombre_equipo}' ahora está disponible.")
            actualizar_tabla()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar el estado:\n{e}")

    tk.Button(frame_botones, text="Marcar como disponible", bg="#FFA000", fg="white",
              font=("Arial", 11, "bold"), width=20, relief="flat",
              command=marcar_disponible).pack(side="left", padx=10)

    def regresar():
        ventana.destroy()

    tk.Button(frame_botones, text="Regresar al menú", bg="#D32F2F", fg="white",
              font=("Arial", 11, "bold"), width=18, relief="flat",
              command=regresar).pack(side="left", padx=10)

    ventana.mainloop()
    conexion.close()
