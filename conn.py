import sqlite3

def conectar():
    conexion = sqlite3.connect("prestamos.db")
    return conexion