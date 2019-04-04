from .models import Usuario


def usuarioLogueado(request):
    usuario = None
    if "cod_cuenta" in request.session:
        codigo = request.session["cod_cuenta"]
        usuario = Usuario.objects.filter(cod_usuario=codigo).first()
    return {
        'usuario_logueado': usuario,
    }