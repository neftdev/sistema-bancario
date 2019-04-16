from django.test import Client, TestCase, SimpleTestCase
from .models import Usuario, Rol, Credito


class UsuarioLoginTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rol1 = Rol(nombre="Administrador", descripcion=" ")
        cls.rol1.save()
        cls.rol2 = Rol(nombre="Cliente", descripcion=" ")
        cls.rol2.save()
        Usuario(
            num_cuenta=10001,
            full_name="admin",
            nick_name="admin",
            correo="admin@gmail.com",
            password="12121212",
            monto="1000",
            rol=cls.rol1
        ).save()
        Usuario(
            num_cuenta=10002,
            full_name="ronald",
            nick_name="ronald",
            correo="ronald@gmail.com",
            password="12345678",
            monto="1000",
            rol=cls.rol2
        ).save()
        Usuario(
            num_cuenta=10003,
            full_name="mario",
            nick_name="mario",
            correo="mario@gmail.com",
            password="12345678",
            monto="1000",
            rol=cls.rol2
        ).save()

    def test_login_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200,
                         'Peticion incorrecta al login')

    def test_login_comprobacion_de_usuario_no_existente(self):
        # Peticion post al login
        response = self.client.post(
            '/login', {'cod_usuario': 45, 'password': '12345678', 'nick_name': 'ronald'})

        # Como el codigo de usuario no es le correcto el usuario no deberia loguearse
        self.assertEqual(response.status_code, 200,
                         'No deberia ingresar ya el codigo de usuario no es el correcto')

    def test_login_cliente(self):
        # Se realiza una peticion post con un usuario existente
        response = self.client.post(
            '/login', {'cod_usuario': 2, 'password': '12345678', 'nick_name': 'ronald'})

        # Los datos deben ser correctos, por lo tanto se tiene que mostrar la pagina de inicio
        # Debe mostrar el home para el cliente
        self.assertRedirects(
            response, '/home', status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )

    def test_login_admin(self):
        # Se realiza una peticion post con un datos de usuario administrador
        response = self.client.post(
            '/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})

        # Debe mostra el home para el administrador
        self.assertRedirects(
            response, '/admin/home', status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )

    def test_verificar_acceso_a_paginas_admin(self):
        response = self.client.post(
            '/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})
        response = self.client.get('/admin/acreditar')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina acreditar')
        response = self.client.get('/admin/debitar')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina debitar')
        response = self.client.get('/admin/home')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina admin.home')
        response = self.client.get('/admin/reportes/usuarios')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina reporte.usuarios')
        response = self.client.get('/admin/reportes/creditos')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina reporte.creditos')

    def test_verificar_acceso_a_paginas_cliente(self):
        response = self.client.post(
            '/login', {'cod_usuario': 2, 'password': '12345678', 'nick_name': 'ronald'})
        response = self.client.get('/codigo')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina codigo')
        response = self.client.get('/transferencia')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina de transferencia')
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina home')
        response = self.client.get('/credito')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina de creditos')

    # ***********************************************TESTS DE REGISTRO

    def test_registro_get(self):
        response = self.client.get('/registro')
        self.assertEqual(response.status_code, 200,
                         'Peticion incorrecta al registro')

    def test_registro_post(self):
        # Peticion post al registro enviando datos de formulario
        response = self.client.post('/registro',
                                    {'nick_name': 'prueba1',
                                     'full_name': 'Prueba Unitaria',
                                     'correo': 'prueba@prueba.com',
                                     'password': '12345678',
                                     'confirm_password': '12345678'})

        # Verificar si es valido
        self.assertRedirects(response, '/codigo', status_code=302, target_status_code=200,
                             fetch_redirect_response=True)

    def test_transferencia(self):
        self.client.post('/login', {'cod_usuario': 2, 'password': '12345678', 'nick_name': 'ronald'})
        self.client.post('/transferencia', {'cuenta': 10003, 'monto': 100})
        usuario1 = Usuario.objects.filter(num_cuenta=10002).first()
        usuario2 = Usuario.objects.filter(num_cuenta=10003).first()
        self.assertEquals(usuario1.monto, 900)
        self.assertEquals(usuario2.monto, 1100)

    def test_credito(self):
        self.client.post('/login', {'cod_usuario': 2, 'password': '12345678', 'nick_name': 'ronald'})
        self.client.post('/credito', {'monto': 1000, 'descripcion': 'Prueba'})
        peticion = Credito.objects.all().first()
        self.assertFalse(peticion, None)
        self.assertEquals(peticion.descripcion, 'Prueba')
        self.assertEquals(peticion.cod_estado, 1)
