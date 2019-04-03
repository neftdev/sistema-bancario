from django.shortcuts import render, redirect
from apps_.usuario.models import Usuario, Credito, Debito
from apps_.admin.forms import DebitoForm
import math
# from .models import Debito
# Create your views here.
def acreditarView(request):
    errors = []
    if request.method == 'POST':
        cuenta = request.POST['cuenta']
        monto = request.POST['monto']
        print("Cuenta: "+cuenta)
        verify = Usuario.objects.filter(num_cuenta=cuenta).exists()
        if verify:
            usuario = Usuario.objects.filter(num_cuenta=cuenta).first()
            usuario.monto = str(float(usuario.monto)+float(monto))
            usuario.save()
            print("Monto total: "+str(usuario.monto))
            return render(request, 'admin/acreditar.html', {'exito': True, 'errors': errors})
        else:
            errors.append('La cuenta ingresada no existe. Ingrese una cuenta valida.')
    return render(request, 'admin/acreditar.html', {'errors': errors})

def debitarView(request):
    #if "cod_cuenta" not in request.session or "rol" not in request.session:
    #    return redirect('usuario:login')
    #print("******************Debitar")
    errors = []
    if request.method == 'POST':
        cuenta = request.POST['cuenta']
        verify = Usuario.objects.filter(num_cuenta=cuenta).exists()
        if verify:
            usuario = Usuario.objects.filter(num_cuenta=cuenta).first()
            monto = request.POST['monto']
            diferencia = float(usuario.monto)-float(monto)
            print("diferencia: "+str(diferencia))
            if diferencia > 0.0:
                #MODIFICAR MONTO
                usuario.monto = str(diferencia)
                usuario.save()

                #GUARDAR DEBITO
                descripcion = request.POST['descripcion']
                debit = Debito(cuenta_id = str(usuario.cod_usuario), monto=monto, descripcion=descripcion)
                debit.save()
                return render(request, 'admin/debitar.html', {'exito': True, 'errors': errors})
            else:
                errors.append('El monto ingresado excede la cuenta por '+str(-1*diferencia)+'. Debite un valor menor.')    
        else:
            errors.append('La cuenta ingresada no existe. Ingrese una cuenta valida.')
            
    print("******************/Debitar")
    #form = DebitoForm()
    return render(request, 'admin/debitar.html', {'errors': errors})

def homeView(request):
    print("***************ADMIN")
    if "cod_cuenta" not in request.session or "rol" not in request.session:
       return redirect('usuario:login')

    return render(request, 'admin/index.html')

def aprobarView(request, id_credito=None):
    verify = Credito.objects.filter(cod_credito=id_credito, cod_estado=1).exists()
    if verify:
        credito = Credito.objects.filter(cod_credito=id_credito).first()
        credito.cod_estado_id='2'
        credito.save()

    if "cod_cuenta" not in request.session or "rol" not in request.session:
       return redirect('usuario:login')

    creditos = Credito.objects.filter(cod_estado=1)
    return render(request, 'admin/aprobar.html', {"roles": creditos})

def repUsuariosView(request):
    if "cod_cuenta" not in request.session or "rol" not in request.session:
       return redirect('usuario:login')
    usuarios = Usuario.objects.filter(rol_id=2)
    return render(request, 'admin/reportes/usuarios.html', {"roles": usuarios})

def repCreditosView(request):
    if "cod_cuenta" not in request.session or "rol" not in request.session:
       return redirect('usuario:login')
    creditos = Credito.objects.filter(cod_estado=2)
    return render(request, 'admin/reportes/creditos.html', {"roles": creditos})
