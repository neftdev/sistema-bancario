USE banco_ayd1;

INSERT INTO usuario_rol (nombre, descripcion)
VALUES
("Administrador", "Responsable de aceptar creditos, realizar debitos y de acreditar"),
("Cliente", "Cualquier usuario que se registre");

INSERT INTO usuario_estadocredito (nombre, descripcion)
VALUES
("Pendiente", "En espera de aprobacion."),
("Aprobado", "Se acepto el credito al usuario."),
("Cancelado", "Se rechazo el credito al usuario.");

INSERT INTO usuario_usuario(full_name, nick_name, correo, password, monto, rol_id)
VALUES
("admin", "admin", "admin@gmail.com", "12121212", 0, 1);