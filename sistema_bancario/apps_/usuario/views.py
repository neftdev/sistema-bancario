from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Usuario, Transferencia, Credito, Notificacion, Debito
from .forms import LoginForm, RegisterForm, CreditoForm
from sistema_bancario.util import render_pdf
import time


def codigoView(request):
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 2:
        return redirect('admin:home')
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
        post_values['rol'] = 2
        form = RegisterForm(post_values)
        # print("POST: "+str(post_values))
        if form.is_valid():
            print("VALID")
            usuario = form.save()
            usuario.num_cuenta += usuario.cod_usuario
            usuario.save()
            request.session["cod_cuenta"] = usuario.cod_usuario
            request.session["rol"] = usuario.rol.id
            return redirect('usuario:codigo')
    else:
        form = RegisterForm()
    return render(request, 'register/index.html', {'form': form})


def loginView(request):
    # Borrar variable de sesion
    # print("*******************************LOGIN")
    if "cod_cuenta" in request.session:
        del request.session["cod_cuenta"]
    if "rol" in request.session:
        del request.session["rol"]
    # print("//algo")
    error = None
    if request.method == 'POST':
        codigo = request.POST['cod_usuario']
        name = request.POST['nick_name']
        clave = request.POST['password']

        # print("Codigo: "+codigo+", Name: "+name+", Pass: "+clave)

        verify = Usuario.objects.filter(
            pk=codigo, nick_name=name, password=clave).exists()
        if verify:
            objects = Usuario.objects.filter(
                pk=codigo, nick_name=name, password=clave)
            rol = objects[0].rol.id

            # CREACIONES DE VARIABLE DE SESION
            request.session["cod_cuenta"] = str(objects[0].pk)
            request.session["rol"] = rol
            # print("Rol: #"+str(objects[0].pk)+"#")
            if rol == 1:
                return redirect('admin:home')
            elif rol == 2:
                return redirect('usuario:home')
        else:
            error="Credenciales invalidas"        
    form = LoginForm()
    # print("//algo2")
    return render(request, 'login/index.html', {'form': form,"error": error})


def homeView(request):
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 2:
        return redirect('admin:home')
    codigo = request.session["cod_cuenta"]
    usuario = Usuario.objects.filter(cod_usuario=codigo).first()
    # print("Cc: "+str(request.session["cod_cuenta"]))
    trans_in = Transferencia.objects.filter(destino_cod_usuario_id=
                    request.session["cod_cuenta"]).values("monto", "fecha", "destino_cod_usuario__num_cuenta")
    creditos = Credito.objects.filter(cod_estado_id=2, cod_usuario_id=request.session["cod_cuenta"]).values("monto", "fecha")

    trans_out = Transferencia.objects.filter(origen_cod_usuario_id=
                    request.session["cod_cuenta"]).values("monto", "fecha", "origen_cod_usuario__num_cuenta")   
    debitos = Debito.objects.filter(cuenta_id=request.session["cod_cuenta"]).values("monto", "fecha")

    if usuario is not None:
        return render(request, 'user/index.html', {'usuario': usuario, 
            'trans_in': trans_in, 'creditos': creditos, 
            'trans_out': trans_out, 'debitos': debitos})
    return redirect('usuario:login')


def transferenciaView(request):
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 2:
        return redirect('admin:home')
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
            Notificacion(
                descripcion='La cuenta {} te ha transferido el monto de Q{}.'.format(usuario_origen.num_cuenta, monto),
                url='/home',
                cod_usuario=usuario_destino
            ).save()
            return render(request, 'user/transferencia.html', {'exito': exito, 'errors': errors})

    return render(request, 'user/transferencia.html', {'errors': errors})


def creditoView(request):
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 2:
        return redirect('admin:home')
    exito = False
    codigo_usuario = request.session["cod_cuenta"]

    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['cod_usuario'] = codigo_usuario
        post_values['cod_estado'] = 1
        form = CreditoForm(post_values)
        if form.is_valid():
            usuariosAdmin = Usuario.objects.filter(rol_id=1)
            usuario = Usuario.objects.filter(cod_usuario=codigo_usuario).first()
            descrip = 'La cuenta {} ha solicitado un credito.'.format(usuario.num_cuenta)
            url = '/admin/aprobar/0'
            for admin in usuariosAdmin:
                Notificacion(
                    descripcion= descrip,
                    url=url,
                    cod_usuario=admin
                ).save()
            form.save()
            exito = True
            form = CreditoForm()            

    else:
        form = CreditoForm()
    creditos = Credito.objects.filter(cod_usuario_id=codigo_usuario)
    return render(request, 'user/credito.html', {'form': form, 'exito': exito, 'creditos': creditos})

def notificacion_delete(request, cod_notificacion):
    notificacion = get_object_or_404(Notificacion, pk=cod_notificacion)
    if request.method == 'POST':
        url = notificacion.url
        notificacion.delete()
        return redirect(url)
    if request.session["rol"] == 1:
        return redirect('admin:home')
    return redirect('usuario:home')


def crear_reporte(request):
    if "cod_cuenta" not in request.session or "rol" not in request.session:
    return redirect('usuario:login')
    if request.session["rol"] != 2:
        return redirect('admin:home')
    codigo = request.session["cod_cuenta"]
    usuario = Usuario.objects.filter(cod_usuario=codigo).first()

    trans_enviadas = Transferencia.objects.filter(origen_cod_usuario=usuario)
    total_trans_env = trans_enviadas.aggregate(Sum('monto'))

    trans_recibidas = Transferencia.objects.filter(destino_cod_usuario=usuario)
    total_trans_rec = trans_recibidas.aggregate(Sum('monto'))

    creditos = Credito.objects.filter(cod_usuario=usuario).filter(cod_estado_id=2)
    total_creditos = creditos.aggregate(Sum('monto'))

    debitos = Debito.objects.filter(cuenta=usuario)
    total_debitos = debitos.aggregate(Sum('monto'))

    fecha = time.strftime("%c")

    pdf = render_pdf("user/reporte.html", {
        "usuario": usuario,
        "trans_enviadas": trans_enviadas,
        "trans_recibidas": trans_recibidas,
        "creditos": creditos,
        "debitos": debitos,
        "total_trans_env": total_trans_env,
        "total_trans_rec": total_trans_rec,
        "total_creditos": total_creditos,
        "total_debitos": total_debitos,
        "fecha": fecha
    })
    return HttpResponse(pdf, content_type="application/pdf")
