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

Servidor Local
--------------

    python manage.py runserver

