CREATE TABLE cursos (
    id_curso SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    profesor_id INTEGER REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

