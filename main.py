from menu import mostrar_menu
from menu_admin import menu_admin

def main(usuario_sesion):
    """
    Recibe el diccionario de sesion devuelto por main_login.py
    """
    tipo = usuario_sesion["tipo"]
    rol = usuario_sesion["rol"]
    id_usuario = usuario_sesion["id"]
    nombre = usuario_sesion["nombre"]

    if tipo == "alumno":
        mostrar_menu(nombre, id_usuario)
    elif tipo == "usuario":
        menu_admin(nombre, rol, id_usuario)
    else:
        print("Rol no reconocido. Acceso denegado.")

if __name__ == "__main__":
    print("Este archivo debe ser llamado desde main_login.py")
