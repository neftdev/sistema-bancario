from django.shortcuts import render, redirect
from apps_.usuario.models import Usuario
# from .models import Debito
from .forms import AcreditarForm
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
    form = AcreditarForm()
    return render(request, 'admin/acreditar.html', {'form': form})

def homeView(request):
    #if "cod_cuenta" not in request.session or "rol" not in request.session:
    #    return redirect('usuario:login')

    return render(request, 'admin/index.html')