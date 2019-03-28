## Actualizar
sudo apt-get update

## Instalando algunas cosas de python xD....
sudo apt-get install build-essential python-dev python-setuptools

## Instalando pip
sudo easy_install pip

## Actualizando pip
sudo pip install --upgrade pip

## Instalando virtualenv para entornos virtuales
sudo pip install virtualenv

## Creando entorno virtual
virtualenv env --python=python3

## Me muevo a la carpeta env
cd env

## Activando el entorno virtual
source bin/activate

## Instalando django
pip install Django==2.1.7

# ## Regresando a la carpeta anterior
# cd ..

# ## Creando proyecto de django, cambia el nombre www por el de tu proyecto
# django-admin.py startproject www

# ## Moviendome a la carpeta del proyecto, cambie el nombre al de tu proyecto
# cd www

# ## Dando le permisos al archivo manage.py
# chmod +x manage.py

# ## desactivar entorno
# deactivate
