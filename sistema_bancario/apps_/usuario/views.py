from django.shortcuts import render, redirect
from .models import Usuario
from .forms import LoginForm, RegisterForm


def registroView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            request.session["cod_cuenta"] = form.cleaned_data.get('cod_usuario')
            return redirect('home:index')
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
        
        print("Codigo: "+codigo+", Name: "+name+", Pass: "+clave)

        verify = Usuario.objects.filter(
            pk=codigo, nick_name=name, password=clave).exists()

        if verify:
            objects = Usuario.objects.filter(pk=codigo, nick_name=name, password = clave)
            rol = str(objects[0].rol.nombre);
            
            #CREACIONES DE VARIABLE DE SESION
            request.session["cod_cuenta"] = str(objects[0].pk)

            print("Rol: #"+str(objects[0].pk)+"#")
            if rol == 'administrador':
                return redirect('admin_:perfil')
            elif rol == 'cliente':
                return redirect('usuario:home')

    form = LoginForm()
    return render(request, 'login/index.html', {'form': form})

def homeView(request):
    if "cod_cuenta" not in request.session:
        return redirect('usuario:login')

    return render(request, 'user/index.html')