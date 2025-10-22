from conn import conectar
import sqlite3

def pedir_prestamo(id_alumno):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_equipo, nombre_equipo, serie_equipo, estado 
        FROM equipos 
        WHERE estado = 'Disponible'
    """)
    equipos = cursor.fetchall()

    if not equipos:
        print("\n No hay equipos disponibles para prestamo.")
        conexion.close()
        return

    print("\n|=== Equipos disponibles ===|")
    print("{:<5} {:<25} {:<15} {:<15}".format("ID", "Nombre", "Serie", "Estado"))
    print("-"*65)
    for eq in equipos:
        id_eq, nombre, serie, estado = eq
        print("{:<5} {:<25} {:<15} {:<15}".format(id_eq, nombre, serie, estado))

    try:
        id_equipo = int(input("\nIngresa el ID del equipo que desea pedir: "))
    except ValueError:
        print("ID inválido.")
        conexion.close()
        return

    cursor.execute("SELECT estado FROM equipos WHERE id_equipo = ?", (id_equipo,))
    resultado = cursor.fetchone()
    if not resultado:
        print("No existe ese equipo.")
        conexion.close()
        return

    estado_actual = resultado[0]
    if estado_actual != "Disponible":
        print("El equipo no esta disponible.")
        conexion.close()
        return

    try:
        cursor.execute("""
            INSERT INTO prestamos (id_equipo, id_alumno, devuelto)
            VALUES (?, ?, 'No')
        """, (id_equipo, id_alumno))

        cursor.execute("UPDATE equipos SET estado = 'Prestado' WHERE id_equipo = ?", (id_equipo,))

        conexion.commit()
        print("\nPrestamo registrado correctamente.")
    except sqlite3.Error as e:
        print(f"\nError al registrar el prestamo: {e}")
    finally:
        conexion.close()
