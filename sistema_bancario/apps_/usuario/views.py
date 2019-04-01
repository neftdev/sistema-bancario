from django.shortcuts import render, redirect
from apps_.usuario.models import Usuario
from apps_.usuario.forms import LoginForm
# Create your views here.

def login_view(request):
    #Borrar variable de sesion
    if "cod_cuenta" in request.session:
        del request.session["cod_cuenta"]

    if request.method == 'POST':
        codigo = request.POST['cod_usuario']
        name = request.POST['nick_name']
        clave = request.POST['password']
        
        print("Codigo: "+codigo)

        verify = Usuario.objects.filter(pk=codigo, nick_name=name, password = clave).exists()

        if verify:
            objects = Usuario.objects.filter(cod_usuario=cod_usuario, nick_name=name, password = clave)
            print("Rol: #"+str(objects[0].rol)+"#")
            if str(objects[0].rol) == 'Administrador':
                return redirect('admin_:perfil', str(objects[0].id))
            elif str(objects[0].rol) == 'Cliente':
                return redirect('user_:perfil', str(objects[0].id))
            elif str(objects[0].rol) == 'Call Center':
                return redirect('admin_:center')


    form = LoginForm()
    return render(request, 'login/index.html', {'form': form})