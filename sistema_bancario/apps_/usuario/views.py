from django.shortcuts import render, redirect
from .forms import RegisterForm


def registroView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:index')
    else:
        form = RegisterForm()
    return render(request, 'register/index.html', {'form': form})
