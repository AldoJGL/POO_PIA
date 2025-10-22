from conn import conectar
import hashlib

def verificar_contrasena(contrasena_ingresada, contrasena_guardada):
    return hashlib.sha256(contrasena_ingresada.encode()).hexdigest() == contrasena_guardada

def login():
    conexion = conectar()
    cursor = conexion.cursor()

    correo = input("Ingresa tu correo universitario: ")
    contrasena = input("Ingresa tu contraseña: ")

    cursor.execute("SELECT id_alumno, contrasena, nombre_alumno FROM alumnos WHERE correo = ?", (correo,))
    resultado = cursor.fetchone()

    conexion.close()

    if resultado:
        id_alumno, contrasena_guardada, nombre = resultado

        if verificar_contrasena(contrasena, contrasena_guardada):
            print(f"Bienvenido {nombre.split()[0]}.\n")
            return nombre, id_alumno
        else:
            print("Contraseña incorrecta")
    else:
        print("No existe ese usuario registrado")

    return None
