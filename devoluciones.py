from conn import conectar
import sqlite3

def devolver_equipo(id_alumno):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT p.id_prestamo, e.nombre_equipo, e.serie_equipo, e.estado
        FROM prestamos p
        JOIN equipos e ON p.id_equipo = e.id_equipo
        WHERE p.id_alumno = ? AND p.devuelto = 'No'
    """, (id_alumno,))
    prestamos = cursor.fetchall()

    if not prestamos:
        print("\nNo tienes prestamos activos.")
        conexion.close()
        return

    print("\n|=== Tus prestamos activos ===|")
    print("{:<5} {:<25} {:<15} {:<15}".format("ID", "Nombre", "Serie", "Estado"))
    print("-"*65)
    for pre in prestamos:
        id_pre, nombre, serie, estado = pre
        print("{:<5} {:<25} {:<15} {:<15}".format(id_pre, nombre, serie, estado))

    try:
        id_prestamo = int(input("\nIngrese el ID del prestamo que desea devolver: "))
    except ValueError:
        print("ID inválido.")
        conexion.close()
        return

    cursor.execute("SELECT id_equipo FROM prestamos WHERE id_prestamo = ? AND id_alumno = ? AND devuelto = 'No'", 
                   (id_prestamo, id_alumno))
    resultado = cursor.fetchone()
    if not resultado:
        print("No exste ese prestamo")
        conexion.close()
        return

    id_equipo = resultado[0]

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

        conexion.commit()
        print("\nEquipo devuelto correctamente.")
    except sqlite3.Error as e:
        print(f"\nError al procesar la devolución: {e}")
    finally:
        conexion.close()
