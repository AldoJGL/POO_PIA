from conn import conectar
import sqlite3

def agregar_equipo():
    conexion = conectar()
    cursor = conexion.cursor()

    print("\n|=== Registrar nuevo equipo ===|")

    nombre_equipo = input("Nombre del equipo: ").strip()
    while not nombre_equipo:
        nombre_equipo = input("Nombre del equipo (no puede estar vacio): ").strip()

    serie_equipo = input("Numero/serie del equipo: ").strip()
    while not serie_equipo:
        serie_equipo = input("Numero/serie del equipo (no puede estar vacio): ").strip()

    estado = input("Estado (Disponible / En mantenimiento / Prestado): ").strip()
    if not estado:
        estado = "Disponible"

    descripcion = input("Descripcion: ").strip()

    try:
        cursor.execute("""
            INSERT INTO equipos (nombre_equipo, serie_equipo, estado, descripcion)
            VALUES (?, ?, ?, ?)
        """, (nombre_equipo, serie_equipo, estado, descripcion))

        conexion.commit()
        print("\nEquipo registrado correctamente.")
    except sqlite3.IntegrityError as e:
        print(f"\nError en el numero de serie: {e}")
    except Exception as e:
        print(f"\nError al registrar el equipo: {e}")
    finally:
        conexion.close()

if __name__ == "__main__":
    agregar_equipo()
