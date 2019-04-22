# Sistema Bancario (-AYD1-)

Sistema en línea para que cualquier usuario pueda entrar desde cualquier dispositivo.


Requerimientos
--------------

+ Python 3
+ [Django 2.1](https://docs.djangoproject.com/es/2.1/)


Configuración (Linux)
---------------------

Verificar tener instalado lo siguiente:

    sudo apt-get update
    sudo apt-get install build-essential python-dev python-setuptools

Instalar pip:

    sudo easy_install pip
    sudo pip install --upgrade pip

Instalar virtualenv:

    sudo pip install virtualenv

Crear el entorno virtual para python3:

    virtualenv env --python=python3

Activar entorno:

    cd env
    source bin/activate

Instalar Django

    pip install Django==2.1.x

Iniciar sesion en MySQL por consola

    mysql -u root -p

Crear Nuevo usuario en MySQL

    CREATE USER 'banco'@'localhost' IDENTIFIED BY '44204394';
    // darle privilegios
    GRANT ALL PRIVILEGES ON * . * TO 'nombre_usuario'@'localhost';
    // refrescar privilegios
    FLUSH PRIVILEGES;

Instalar el cliente de MySQL para Python

    pip install pymysql

Modificar el Archivo __init__ de la aplicacion principal

    import pymysql
    pymysql.install_as_MySQLdb()

Configuracion de la base de datos

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nombreDB',
            'USER': 'nombreusuario',
            'PASSWORD': 'pass',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }


Servidor Local
--------------

    python manage.py runserver

