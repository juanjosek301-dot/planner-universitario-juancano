-- Crea la tabla de usuarios
create table usuarios (
  id SERIAL PRIMARY KEY,
  nombre TEXT NOT NULL,
  correo TEXT UNIQUE NOT NULL,
  clave TEXT NOT NULL
); 