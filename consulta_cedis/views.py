from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, ContentType, Group, User
from .models import *
from django.contrib.auth import REDIRECT_FIELD_NAME
from functools import wraps
from django.db import models
from django.shortcuts import resolve_url
from urllib.parse import urlparse
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
#Vistas

##############################################

#Vista de inicio de sesión, devuelve al template de login
def login_page(request):
    return render(request,'login/nlogin.html')

#Vista de login, se ejecuta cuando el usuario presiona el botón 'Iniciar Sesión'
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('user', '')
        password = request.POST.get('password', '')

        #Autenticamos al usuario
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            role = ""
            if user.groups.all().exists():
                usrol = user.groups.all().latest('id')
                role = usrol.name
            login(request, user)
            
            #Colocamos datos en la sesión para mostrar en la pantalla principal
            request.session['rol'] = role
            permissions = Permission.objects.filter(user=request.user)
            request.session['nombre'] = user.first_name+" "+user.last_name
            request.session['fecha'] = str(datetime.today().strftime('%d-%m-%Y'))

            #Devolvemos a la consulta de udis
            return redirect('/cedis/consulta_udis')
        else:
            return render(request,'login/nlogin.html',{'error': True, 'message': 'Nombre de usuario o contraseña incorrecta.'})


##############################################

#Vista de registro, envía al template de registro de usuario
def registro(request):
    return render(request,'login/registro.html')

#Vista de guardado de registro
def registro_guardar(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm-password', '')
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        telefono = request.POST.get('telefono', '')


        if password == confirm_password:
            if not User.objects.filter(username=email).exists():
                
                user = User.objects.create_user(username=email,email=email,password=password,first_name=nombre,last_name=apellido)

                #Cada usuario nuevo entra con el rol de capturista
                group = Group.objects.get(name='Capturista')
                user.groups.add(group)
                user.save()
                
                return render(request,'login/nlogin.html',{'error': False,'registro': True, 'message': 'Usuario registrado. Ya puedes iniciar sesión.'})
            else:
                return render(request,'login/registro.html',{'error': True, 'message': 'Ya existe un registro con el correo electrónico ingresado. Recupera tu contraseña.'})   
        else:
            return render(request,'login/registro.html',{'error': True, 'message': 'La contraseña no coincide.'})
    else:
        return redirect('/cedis/consulta_udis')


##############################################

#Vista para terminar sesión, envía al login de vuelta
@login_required(login_url='/cedis/login')
def logout_user(request):
    logout(request)
    return redirect('/cedis/login')


##############################################

def permission_required_2(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        #return HttpResponseNotFound()
        return False
    return user_passes_test_2(check_perms, login_url=login_url)


def user_passes_test_2(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                #if request.user.is_authenticated:
                #    return HttpResponseNotFound()
                return view_func(request, *args, **kwargs)
            if request.user.is_authenticated:
                return HttpResponseNotFound()
            else:
                path = request.build_absolute_uri()
                resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
                # If the login url is the same scheme and net location then just
                # use the path as the "next" url.
                login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
                current_scheme, current_netloc = urlparse(path)[:2]
                if ((not login_scheme or login_scheme == current_scheme) and
                        (not login_netloc or login_netloc == current_netloc)):
                    path = request.get_full_path()
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(
                    path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator

##############################################

#Vista de consulta de udis, devuelve a la página para consultar los udis
@login_required(login_url='/cedis/login')
def consulta_udis(request):
    hoy = datetime.today().strftime("%d-%m-%Y")
    return render(request,'udis/home.html',{'hoy':hoy})


##############################################

#Vista de consulta de udis, devuelve a la página para consultar las tiie
@login_required(login_url='/cedis/login')
def consulta_tiie(request):
    hoy = datetime.today().strftime("%d-%m-%Y")
    return render(request,'tiie/home.html',{'hoy':hoy})


##############################################

#Vista de consulta de historial de busquedas
@login_required(login_url='/cedis/login')
def historial_busquedas(request):
    hoy = datetime.today().strftime("%d-%m-%Y")

    #Obtenemos datos de información
    objConsultas = Consulta.objects.filter(user=request.user)
    busquedas_hoy = objConsultas.filter(created__gte=datetime.now().replace(hour=0,minute=0,second=0)).count()
    busquedas_totales = objConsultas.count()

    return render(request,'historial/home.html',{'consultas':objConsultas,'busquedas_hoy':busquedas_hoy,'busquedas_totales':busquedas_totales})

#Vista para guardar consultas
def guardar_consulta(request):
    try:
        message = {"error": False, "message": "", "data": []}
        
        fecha_inicial = request.POST.get('fecha_inicial','')
        fecha_final = request.POST.get('fecha_final','')
        tipo = request.POST.get('tipo','1')

        objConsulta = Consulta.objects.create()
        objConsulta.user = request.user
        objConsulta.fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%d")
        objConsulta.fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")
        objConsulta.tipo = tipo
        objConsulta.save()


        message['message'] = "ok"
        return JsonResponse(message)
    except Exception as e:
        message['message'] = e
        message['error'] = True
        return JsonResponse(message)

    