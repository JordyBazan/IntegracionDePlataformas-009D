from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from .views import iniciar_transaccion, completar_transaccion

urlpatterns = [
    path('', views.CargarInicio, name='home'),
    path('catalogo',views.CargarCatalogo),
    path('Nosotros',views.CargarNosotros),
    path('carrito',views.CargarCarrito),
    path('Contactanos.html',views.CargarContactanos),
    path('fundación',views.CargarFundacion),
    path('guapeton',views.CargarGuapeton),
    path('clima',views.CargarClima),

    
    path('agregarProducto',views.cargarAgregarProd),
    path('FormularioAgregarProd',views.agregarProducto),
    
    
    path('editarProducto/<sku>',views.cargarEditarProducto),
    path('editarProducto',views.editarProducto),
    path('eliminarProducto/<codigo_producto>',views.eliminarProducto),


    ##path('admin/', admin.site.urls),
    
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),

    ##path('carrito',views.carrito)

    path('obtenerProducto',views.obtenerProducto,name='obtenerProducto'),
    path('actualizarStock',views.actualizarStock),
    path('transbank/iniciar-transaccion/', iniciar_transaccion, name='iniciar_transaccion'),
    path('transbank/completar-transaccion/', completar_transaccion, name='completar_transaccion'),
]
 