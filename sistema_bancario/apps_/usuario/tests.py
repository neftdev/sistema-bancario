from django.test import Client, TestCase, SimpleTestCase
from .models import Usuario, Rol, Credito, EstadoCredito


class UsuarioLoginTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.est1 = EstadoCredito(nombre="Pendiente", descripcion="En espera de aprobacion.")
        cls.est1.save()
        cls.est2 = EstadoCredito(nombre="Aprobado", descripcion="Se acepto el credito al usuario.")
        cls.est2.save()
        cls.est3 = EstadoCredito(nombre="Cancelado", descripcion="Se rechazo el credito al usuario.")
        cls.est3.save()

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
        cls.us2 = Usuario(
            num_cuenta=10002, full_name="ronald", nick_name="ronald", correo="ronald@gmail.com", 
            password="12345678", monto="1000", rol=cls.rol2)
        cls.us2.save()
        cls.us3 = Usuario(
            num_cuenta=10003, full_name="mario", nick_name="mario", correo="mario@gmail.com",
            password="12345678", monto="1000",rol=cls.rol2)
        cls.us3.save()

        #CREDITOS
        Credito(
            monto = "100", descripcion = "Prueba1", fecha = "2015/05/05",
            cod_usuario = cls.us2, cod_estado = cls.est1).save()
        Credito(
            monto = "100", descripcion = "Prueba2", fecha = "2015/05/05",
            cod_usuario = cls.us2, cod_estado = cls.est1).save()

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

    def test_verificar_acceso_a_user_codigo(self):
        self.client.post('/login', {'cod_usuario': 2, 'password': '12345678', 'nick_name': 'ronald'})
        response = self.client.get('/codigo')
        self.assertEqual(response.status_code, 200,'No funciona la pagina codigo')

    def test_verificar_acceso_a_user_transferencia(self):
        self.client.post('/login', {'cod_usuario': 2, 'password': '12345678', 'nick_name': 'ronald'})
        response = self.client.get('/transferencia')
        self.assertEqual(response.status_code, 200, 'No funciona la pagina de transferencia')

    def test_verificar_acceso_a_user_home(self):
        self.client.post('/login', {'cod_usuario': 2, 'password': '12345678', 'nick_name': 'ronald'})
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200, 'No funciona la pagina home')

    def test_verificar_acceso_a_user_creditos(self):
        self.client.post('/login', {'cod_usuario': 2, 'password': '12345678', 'nick_name': 'ronald'})        
        response = self.client.get('/credito')
        self.assertEqual(response.status_code, 200, 'No funciona la pagina de creditos')

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
        peticion = Credito.objects.filter(pk=3).first()
        
        self.assertEquals(peticion.descripcion, 'Prueba')
        self.assertEquals(peticion.cod_estado_id, 1)

    #********************************************************ADMIN

    def test_login_admin(self):
        # Se realiza una peticion post con un datos de usuario administrador
        response = self.client.post(
            '/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})

        # Debe mostra el home para el administrador
        self.assertRedirects(
            response, '/admin/home', status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )

    def test_verificar_acceso_a_admin_acreditar(self):
        self.client.post('/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})
        response = self.client.get('/admin/acreditar')
        self.assertEqual(response.status_code, 200, 'No funciona la pagina acreditar')

    def test_verificar_acceso_a_admin_debitar(self):
        self.client.post('/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})
        response = self.client.get('/admin/debitar')
        self.assertEqual(response.status_code, 200, 'No funciona la pagina debitar')

    def test_verificar_acceso_a_admin_home(self):
        self.client.post('/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})
        response = self.client.get('/admin/home')
        self.assertEqual(response.status_code, 200, 'No funciona la pagina admin.home')

    def test_verificar_acceso_a_admin_reporte_usuarios(self):
        self.client.post('/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})
        response = self.client.get('/admin/reportes/usuarios')
        self.assertEqual(response.status_code, 200, 'No funciona la pagina reporte.usuarios')

    def test_verificar_acceso_a_admin_creditos_aprobados(self):
        self.client.post('/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})
        response = self.client.get('/admin/reportes/creditos-aprobados')
        self.assertEqual(response.status_code, 200, 'No funciona la pagina reporte.creditos')

    def test_verificar_acceso_a_admin_creditos_cancelados(self):
        self.client.post('/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})        
        response = self.client.get('/admin/reportes/creditos-cancelados')
        self.assertEqual(response.status_code, 200, 'No funciona la pagina reporte.creditos')
        

    # ***********************************************TESTS DE ADMIN
    def test_acreditar(self):
        response = self.client.post('/login', 
                                {   'cod_usuario': 1, 
                                    'password': '12121212', 
                                    'nick_name': 'admin'})
        self.client.post('/admin/acreditar', {'cuenta': 10003, 'monto': 100})
        usuario = Usuario.objects.filter(num_cuenta=10003).first()
        self.assertEquals(usuario.monto, 1100)

    def test_debitar(self):
        response = self.client.post('/login', 
                                {   'cod_usuario': 1, 
                                    'password': '12121212', 
                                    'nick_name': 'admin'})
        self.client.post('/admin/debitar', {'cuenta': 10003, 'monto': 100, "descripcion": "Prueba"})
        usuario = Usuario.objects.filter(num_cuenta=10003).first()
        self.assertEquals(usuario.monto, 900)

    def test_eliminar_usuario(self):
        response = self.client.post('/login', 
                                {   'cod_usuario': 1, 
                                    'password': '12121212', 
                                    'nick_name': 'admin'})
        self.client.get('/admin/reportes/usuarios/eliminar/2')
        usuarios = Usuario.objects.filter(rol_id=2).count()
        self.assertEquals(usuarios, 1)

    def test_aprobar_cancelar_credito(self):
        response = self.client.post('/login', 
                                {   'cod_usuario': 1, 
                                    'password': '12121212', 
                                    'nick_name': 'admin'})
        self.client.get('/admin/aprobar/1')
        self.client.get('/admin/cancelar/2')
        cred1 = Credito.objects.filter(pk=1).first()
        cred2 = Credito.objects.filter(pk=2).first()
        self.assertEquals(cred1.cod_estado_id, 2)
        self.assertEquals(cred2.cod_estado_id, 3)
