from consultar import consultar_equipos
from prestamo import pedir_prestamo
from devoluciones import devolver_equipo

def mostrar_menu(nombre, id_alumno):
    while True:
        print(f"\n|--- Menu Principal ({nombre}) ---|")
        print("1. Consultar equipos disponibles")
        print("2. Pedir prestamo de equipo")
        print("3. Devolver equipo")
        print("4. Cerrar sesion")

        opcion = input("Selecciona una opcion: ")

        if opcion == "1":
            consultar_equipos()
        elif opcion == "2":
            pedir_prestamo(id_alumno)
        elif opcion == "3":
            devolver_equipo(id_alumno)
        elif opcion == "4":
            print("Cerrando sesion...\n")
            break
        else:
            print("Opcion no valida")
