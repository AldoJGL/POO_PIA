from conn import conectar

def mostrar_tabla(equipos):
    print("\n{:<5} {:<25} {:<15} {:<15} {:<30}".format("ID", "Nombre", "Serie", "Estado", "Descripción"))
    print("-"*95)
    for eq in equipos:
        id_eq, nombre, serie, estado, desc = eq
        print("{:<5} {:<25} {:<15} {:<15} {:<30}".format(id_eq, nombre, serie, estado, desc))

def consultar_equipos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_equipo, nombre_equipo, serie_equipo, estado, descripcion FROM equipos")
    equipos = cursor.fetchall()

    if not equipos:
        print("\nNo hay equipos registrados.")
        conexion.close()
        return

    print("\n|=== Todos los equipos registrados ===|")
    mostrar_tabla(equipos)

    while True:
        busqueda = input("\nIngrese el nombre a buscar (o presione Enter para salir): ").strip()
        if busqueda == "":
            break

        cursor.execute("""
            SELECT id_equipo, nombre_equipo, serie_equipo, estado, descripcion
            FROM equipos
            WHERE nombre_equipo LIKE ?
        """, ('%' + busqueda + '%',))

        resultados = cursor.fetchall()

        if resultados:
            print(f"\n|=== Resultados para '{busqueda}' ===|")
            mostrar_tabla(resultados)
        else:
            print(f"\nNo se encontraron equipos con '{busqueda}'.")

    conexion.close()

if __name__ == "__main__":
    consultar_equipos()
