from django.shortcuts import render, redirect
from apps_.usuario.models import Usuario, Credito, Debito
from .forms import DebitoForm
import math
# from .models import Debito
# Create your views here.


def acreditarView(request):
    # VALIDAR ACCESO
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 1:
        return redirect('usuario:login')
    ##
    errors = []
    if request.method == 'POST':
        cuenta = request.POST['cuenta']
        monto = request.POST['monto']
        #print("Cuenta: "+cuenta)
        verify = Usuario.objects.filter(num_cuenta=cuenta).exists()
        if verify:
            usuario = Usuario.objects.filter(num_cuenta=cuenta).first()
            usuario.monto = str(float(usuario.monto)+float(monto))
            usuario.save()
            #print("Monto total: "+str(usuario.monto))
            return render(request, 'admin/acreditar.html', {'exito': True, 'errors': errors})
        else:
            errors.append(
                'La cuenta ingresada no existe. Ingrese una cuenta valida.')
    return render(request, 'admin/acreditar.html', {'errors': errors})


def debitarView(request):
    # ************************************************VALIDAR ACCESO
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 1:
        return redirect('usuario:login')
    ##
    errors = []
    if request.method == 'POST':
        cuenta = request.POST['cuenta']
        verify = Usuario.objects.filter(num_cuenta=cuenta).exists()
        if verify:
            usuario = Usuario.objects.filter(num_cuenta=cuenta).first()
            monto = request.POST['monto']
            diferencia = float(usuario.monto)-float(monto)
            #print("diferencia: "+str(diferencia))
            if diferencia > 0.0:
                # MODIFICAR MONTO
                usuario.monto = str(diferencia)
                usuario.save()

                # GUARDAR DEBITO
                descripcion = request.POST['descripcion']
                debit = Debito(cuenta_id=str(usuario.cod_usuario),
                               monto=monto, descripcion=descripcion)
                debit.save()
                return render(request, 'admin/debitar.html', {'exito': True, 'errors': errors})
            else:
                errors.append('El monto ingresado excede la cuenta por ' +
                              str(-1*diferencia)+'. Debite un valor menor.')
        else:
            errors.append(
                'La cuenta ingresada no existe. Ingrese una cuenta valida.')

    # print("******************/Debitar")
    return render(request, 'admin/debitar.html', {'errors': errors})


def homeView(request):
    # print("***************ADMIN")
    # ************************************************VALIDAR ACCESO
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 1:
        return redirect('usuario:login')
    ##
    return render(request, 'admin/index.html')


def aprobarView(request, id_credito=None):
    # ************************************************VALIDAR ACCESO
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 1:
        return redirect('usuario:login')
    ##
    verify = Credito.objects.filter(
        cod_credito=id_credito, cod_estado=1).exists()
    if verify:
        credito = Credito.objects.filter(cod_credito=id_credito).first()
        credito.cod_estado_id = '2'
        credito.save()
        usuario = credito.cod_usuario
        usuario.monto += credito.monto
        usuario.save()
        return redirect('admin:rep_creditos')

    creditos = Credito.objects.filter(cod_estado=1)
    return render(request, 'admin/aprobar.html', {"roles": creditos})


def cancelarView(request, id_credito=None):
    # ************************************************VALIDAR ACCESO
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 1:
        return redirect('usuario:login')
    ##
    verify = Credito.objects.filter(
        cod_credito=id_credito, cod_estado=1).exists()
    if verify:
        credito = Credito.objects.filter(cod_credito=id_credito).first()
        credito.cod_estado_id = '3'
        credito.save()
        return redirect('admin:rep_creditos_cancelados')

    creditos = Credito.objects.filter(cod_estado=1)
    return render(request, 'admin/aprobar.html', {"roles": creditos})


def repUsuariosView(request):
    # ************************************************VALIDAR ACCESO
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 1:
        return redirect('usuario:login')
    ##
    usuarios = Usuario.objects.filter(rol_id=2)
    return render(request, 'admin/reportes/usuarios.html', {"roles": usuarios})


def eliminarUsuarioView(request, cod_usuario=None):
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    verify = Usuario.objects.filter(pk=cod_usuario).exists()
    if verify:
        credito = Usuario.objects.get(pk=cod_usuario).delete()
    usuarios = Usuario.objects.filter(rol_id=2)
    return render(request, 'admin/reportes/usuarios.html', {"roles": usuarios})


def repCreditosView(request):
    # ************************************************VALIDAR ACCESO
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 1:
        return redirect('usuario:login')
    ##
    creditos = Credito.objects.filter(cod_estado=2)
    return render(request, 'admin/reportes/creditos.html', {"roles": creditos, "titulo": "aprobados"})


def repCreditosCanceladosView(request):
    # ************************************************VALIDAR ACCESO
    if "cod_cuenta" not in request.session or "rol" not in request.session:
        return redirect('usuario:login')
    if request.session["rol"] != 1:
        return redirect('usuario:login')
    ##
    creditos = Credito.objects.filter(cod_estado=3)
    return render(request, 'admin/reportes/creditos.html', {"roles": creditos, "titulo": "cancelados"})
