from django.shortcuts import render, redirect
from .models import Usuario, Transferencia, Credito
from .forms import LoginForm, RegisterForm, CreditoForm


def codigoView(request):
    if "cod_cuenta" not in request.session:
        return redirect('usuario:login')
    codigo = request.session["cod_cuenta"]
    usuario = Usuario.objects.filter(cod_usuario=codigo).first()
    if usuario is None:
        return redirect('usuario:login')
    return render(request, 'register/codigo.html', {
        'codigo': usuario.cod_usuario, 'cuenta': usuario.num_cuenta
    })


def registroView(request):
    # num_cuenta
    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['num_cuenta'] = 10000
        form = RegisterForm(post_values)
        if form.is_valid():
            usuario = form.save()
            usuario.num_cuenta += usuario.cod_usuario
            usuario.save()
            request.session["cod_cuenta"] = usuario.cod_usuario
            return redirect('usuario:codigo')
    else:
        form = RegisterForm()
    return render(request, 'register/index.html', {'form': form})


def loginView(request):
    # Borrar variable de sesion
    if "cod_cuenta" in request.session:
        del request.session["cod_cuenta"]
    if "rol" in request.session:
        del request.session["rol"]

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
            rol = objects[0].rol.id

            # CREACIONES DE VARIABLE DE SESION
            request.session["cod_cuenta"] = str(objects[0].pk)
            
            print("Rol: #"+str(objects[0].pk)+"#")
            if rol == 1:
                request.session["rol"] = True
                return redirect('admin:home')
            elif rol == 2:
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

        if not(monto >= 0 and monto <= usuario_origen.monto):
            errors.append(
                'El monto ingresado no es valido. Verifique que no sea negativo o mayor a su saldo actual.')

        codigo_destino = request.POST['cuenta']

        usuario_destino = Usuario.objects.filter(
            num_cuenta=codigo_destino).first()
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
            transferencia = Transferencia(
                monto=monto, origen_cod_usuario=usuario_origen, destino_cod_usuario=usuario_destino
            )
            transferencia.save()
            return render(request, 'user/transferencia.html', {'exito': exito, 'errors': errors})

    return render(request, 'user/transferencia.html', {'errors': errors})


def creditoView(request):
    if "cod_cuenta" not in request.session:
        return redirect('usuario:login')

    exito = False
    codigo_usuario = request.session["cod_cuenta"]

    creditos = Credito.objects.filter(cod_usuario_id=codigo_usuario)

    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['cod_usuario'] = codigo_usuario
        post_values['cod_estado'] = 1
        form = CreditoForm(post_values)
        if form.is_valid():
            form.save()
            exito = True
            form = CreditoForm()

    else:
        form = CreditoForm()
    return render(request, 'user/credito.html', {'form': form, 'exito': exito, 'creditos': creditos})
