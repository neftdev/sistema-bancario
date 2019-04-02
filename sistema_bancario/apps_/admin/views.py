from django.shortcuts import render, redirect
from apps_.usuario.models import Usuario, Credito
from apps_.admin.forms import DebitoForm
# from .models import Debito
# Create your views here.
def acreditarView(request):
#     if "cod_cuenta" not in request.session or "rol" not in request.session:
#         return redirect('usuario:login')
    if request.method == 'POST':
        cuenta = request.POST['cuenta']
        monto = request.POST['monto']
        verify = Usuario.objects.filter(pk=cuenta).exists()
        if verify:
            usuario = Usuario.objects.filter(pk=cuenta).first()
            usuario.monto = str(float(usuario.monto)+float(monto))
            usuario.save()
            print("Monto total: "+str(usuario.monto))
            return redirect('admin:home')
    return render(request, 'admin/acreditar.html')

def debitarView(request):
    #if "cod_cuenta" not in request.session or "rol" not in request.session:
    #    return redirect('usuario:login')
    if request.method == 'POST':
        form = DebitoForm(request.POST)
        if form.is_valid():
            monto = request.POST['monto']
            cuenta = request.POST['cuenta']
            verify = Usuario.objects.filter(pk=cuenta).exists()
            if verify:
                usuario = Usuario.objects.filter(pk=cuenta).first()
                usuario.monto = str(float(usuario.monto)-float(monto))
                usuario.save()
                form.save()
                return redirect('admin:home')
    form = DebitoForm()
    return render(request, 'admin/debitar.html', {'form': form})

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