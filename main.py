from login import login
from menu import mostrar_menu

def main():
    print("|=== Sistema de Prestamo de Equipos ===|\n")
    id_alumno, usuario = login()

    if usuario:
        mostrar_menu(usuario, id_alumno)
    else:
        print("No se pudo iniciar sesion.\n")

if __name__ == "__main__":
    main()