from django.shortcuts import render, redirect
from .models import Usuario
from .forms import LoginForm, RegisterForm


def codigoView(request):
    if "cod_cuenta" not in request.session:
        return redirect('usuario:login')
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

        print("Codigo: "+codigo+", Name: "+name+", Pass: "+clave)

        verify = Usuario.objects.filter(
            pk=codigo, nick_name=name, password=clave).exists()

        if verify:
            objects = Usuario.objects.filter(
                pk=codigo, nick_name=name, password=clave)
            rol = str(objects[0].rol.nombre)

            # CREACIONES DE VARIABLE DE SESION
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
    codigo = request.session["cod_cuenta"]
    usuario = Usuario.objects.filter(cod_usuario=codigo).first()
    if usuario is not None:
        return render(request, 'user/index.html', {'usuario': usuario})
    return redirect('usuario:login')


def transferenciaView(request):
    if "cod_cuenta" not in request.session:
        return redirect('usuario:login')

    errors = []
    
    if request.method == 'POST':
        codigo_origen = request.session["cod_cuenta"]
        usuario_origen = Usuario.objects.filter(
            cod_usuario=codigo_origen).first()

        if usuario_origen is None:
            return redirect('usuario:login')

        monto = int(request.POST['monto'])

        if not(monto > 0 and monto <= usuario_origen.monto):
            errors.append(
                'El monto ingresado no es valido. Verifique que no sea negativo o mayor a su saldo actual.')

        codigo_destino = request.POST['cuenta']

        usuario_destino = Usuario.objects.filter(
            cod_usuario=codigo_destino).first()
        if usuario_destino is None:
            errors.append('El codigo destino no existe o esta vacio.')

        if usuario_origen == usuario_destino:
            errors.append('No puedes transferir saldo a tu misma cuenta.')

        if not errors:
            exito = True
            usuario_origen.monto -= monto
            usuario_destino.monto += monto
            usuario_origen.save()
            usuario_destino.save()
            return render(request, 'user/transferencia.html', {'exito': exito, 'errors': errors})

    return render(request, 'user/transferencia.html', {'errors': errors})
