from .models import Usuario, Notificacion


def usuarioLogueado(request):
    usuario = None
    if "cod_cuenta" in request.session:
        codigo = request.session["cod_cuenta"]
        usuario = Usuario.objects.filter(cod_usuario=codigo).first()
    return {
        'usuario_logueado': usuario,
    }

def get_notificaciones(request):
    notificaciones = None
    if "cod_cuenta" in request.session:
        codigo = request.session["cod_cuenta"]
        notificaciones = Notificacion.objects.filter(cod_usuario_id=codigo)
    return {
        'notificaciones': notificaciones
    }