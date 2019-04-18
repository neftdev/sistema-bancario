from django.test import Client, TestCase, SimpleTestCase
from apps_.usuario.models import Usuario, Rol, Credito, EstadoCredito


class AdminTest(TestCase):
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
            num_cuenta=10001, full_name="admin", nick_name="admin", correo="admin@gmail.com", 
            password="12121212", monto="1000", rol=cls.rol1).save()
        
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
        self.client.post('/login', {'cod_usuario': 1, 'password': '12121212', 'nick_name': 'admin'})
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

        response = self.client.get('/admin/reportes/creditos-aprobados')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina reporte.creditos')
        response = self.client.get('/admin/reportes/creditos-cancelados')
        self.assertEqual(response.status_code, 200,
                         'No funciona la pagina reporte.creditos')
        

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
        #print(Credito.objects.all().count())
        cred1 = Credito.objects.filter(pk=1).first()
        cred2 = Credito.objects.filter(pk=2).first()
        self.assertEquals(cred1.cod_estado_id, 2)
        self.assertEquals(cred2.cod_estado_id, 3)
