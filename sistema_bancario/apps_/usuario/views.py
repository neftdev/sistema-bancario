from django.shortcuts import render, redirect
from .models import Usuario
from .forms import LoginForm
from .forms import RegisterForm


def codigoView(request):
    return render(request, 'register/codigo.html', {'codigo': request.session["cod_cuenta"]})


def registroView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            request.session["cod_cuenta"] = usuario.cod_usuario
            return redirect('usuario:codigo')
    else:
        form = RegisterForm()
    return render(request, 'register/index.html', {'form': form})


def loginView(request):
    # Borrar variable de sesion
    if "cod_cuenta" in request.session:
        del request.session["cod_cuenta"]

    if request.method == 'POST':
        codigo = request.POST['cod_usuario']
        name = request.POST['nick_name']
        clave = request.POST['password']

        print("Codigo: "+codigo)

        verify = Usuario.objects.filter(
            pk=codigo, nick_name=name, password=clave).exists()

        if verify:
            objects = Usuario.objects.filter(
                cod_usuario=cod_usuario, nick_name=name, password=clave)
            print("Rol: #"+str(objects[0].rol)+"#")
            if str(objects[0].rol) == 'Administrador':
                return redirect('admin_:perfil', str(objects[0].id))
            elif str(objects[0].rol) == 'Cliente':
                return redirect('user_:perfil', str(objects[0].id))
            elif str(objects[0].rol) == 'Call Center':
                return redirect('admin_:center')

    form = LoginForm()
    return render(request, 'login/index.html', {'form': form})
