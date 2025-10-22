from conn import conectar

def inicializar():
    conexion = conectar()  
    cursor = conexion.cursor()
    
    with open("estructura.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    
    cursor.executescript(sql_script)
    conexion.commit()
    conexion.close()
    print("Base de datos y tablas creadas correctamente.")

if __name__ == "__main__":
    inicializar()
