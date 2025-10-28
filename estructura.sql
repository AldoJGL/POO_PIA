CREATE TABLE alumnos (
    id_alumno INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_alumno TEXT NOT NULL,
    correo VARCHAR NOT NULL,
    contrasena TEXT NOT NULL
);

CREATE TABLE equipos (
    id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_equipo TEXT NOT NULL,
    serie_equipo INTEGER NOT NULL,
    estado TEXT NOT NULL,
    descripcion VARCHAR
);

CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT NOT NULL,
    rol VARCHAR NOT NULL,
    correo_usuario VARCHAR NOT NULL,
    contrasena_us TEXT NOT NULL
);

CREATE TABLE prestamos (
    id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_equipo INTEGER,
    id_alumno INTEGER,
    fecha_prestamo DATE DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion DATE,
    devuelto TEXT NOT NULL
);

CREATE TABLE mantenimiento (
    id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_equipo INTEGER NOT NULL,
    fecha_mantenimiento DATE DEFAULT CURRENT_TIMESTAMP,
    tipo_mantenimiento VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255),
    costo_mantenimiento DECIMAL(10,2) NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE horarios (
    id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_equipo INTEGER NOT NULL,
    id_alumno INTEGER NOT NULL,
    fecha_prestamo DATE DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion DATE,
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo),
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno)
);
