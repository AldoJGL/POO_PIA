import sqlite3
import hashlib

conn = sqlite3.connect("prestamos.db")
cursor = conn.cursor()

nombre = "Admin Principal"
correo = "admin@gmail.com"
contrasena = "admin123"
rol = "administrador"

contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

cursor.execute("""
    INSERT INTO usuarios(nombre_usuario, rol, correo_usuario, contrasena_us)
    VALUES (?, ?, ?, ?)
""", (nombre, rol, correo, contrasena_hash))

conn.commit()
conn.close()

print("Administrador creado correctamente.")
