from .models import Usuario


def usuarioLogueado(request):
    codigo = request.session["cod_cuenta"]
    usuario = Usuario.objects.filter(cod_usuario=codigo).first()
    return {
        'usuario_logueado': usuario,
    }