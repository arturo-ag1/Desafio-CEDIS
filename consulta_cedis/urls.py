from . import views
from django.urls import include, re_path, path
from django.contrib.auth import views as auth_views
from .views import permission_required_2

urlpatterns = [
    path('recuperacion/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='custom_pass_reset'),
    path('recuperacion/', include('django.contrib.auth.urls')),



    re_path(r'^login/$', views.login_page, name='login_page'),
    re_path(r'^login_user/$', views.login_user, name='login_user'),
    re_path(r'^logout/$', views.logout_user, name='logout_user'),
    re_path(r'^registro/$', views.registro, name='registro'),
    re_path(r'^registro/guardar$', views.registro_guardar, name='registro_guardar'),

    re_path(r'^consulta_udis/$', permission_required_2('cedis.permisos-consulta_udis', login_url='/cedis/login') (views.consulta_udis), name='consulta_udis'),
    re_path(r'^consulta_tiie/$', permission_required_2('cedis.permisos-consulta_tiie', login_url='/cedis/login') (views.consulta_tiie), name='consulta_tiie'),
    
]  