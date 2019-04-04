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


INSERT INTO usuario_usuario(full_name, num_cuenta, nick_name, correo, password, monto, rol_id)
VALUES
("admin", 10001, "admin", "admin@gmail.com", "1234abcd", 0, 1),
("ronald", 10002, "Ronald Berduo", "ronald@gmail.com", "1234abcd", 100, 2),
("mario", 10003, "Mario Morales", "mario@gmail.com", "1234abcd", 100, 2);
