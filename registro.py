from conn import conectar
import hashlib
import re

def hash_contrasena(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validar_correo(correo):
    patron = r"^[\w\.-]+@uanl\.edu\.mx$"
    return re.match(patron, correo) is not None

def registrar_alumno(nombre, correo, contrasena):

    if not validar_correo(correo):
        print("Correo invalido")
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
        print("Alumno registrado correctamente")
    except Exception as e:
        print("Error al registrarte:", e)
    finally:
        conexion.close()

if __name__ == "__main__":
    print("|--- Registrar nuevo alumno ---|")
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    registrar_alumno(nombre, correo, contrasena)
