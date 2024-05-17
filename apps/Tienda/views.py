import json
from django.shortcuts import render, redirect
from .models import *
import os
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from collections import defaultdict
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType

from django.shortcuts import render, redirect
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction



# Create your views here.

def CargarInicio(request):
    return render(request,"index.html")

def CargarNosotros(request):
    return render(request,"Nosotros.html")

def CargarCarrito(request):
    return render(request,"carrito.html")

def CargarContactanos(request):
    return render(request,"Contactanos.html")

def CargarFundacion(request):
    return render(request,"fundación.html")

def CargarGuapeton(request):
    return render(request,"guapeton.html")

def CargarClima(request):
    return render(request,"clima.html")

def CargarCatalogo(request):
    productos = Producto.objects.all()
    cate_producto_flores = Producto.objects.filter(categoriaId = 1)
    cate_producto_herramientas = Producto.objects.filter(categoriaId = 2)
    cate_producto_arboles = Producto.objects.filter(categoriaId = 3)
    cate_producto_maceteros = Producto.objects.filter(categoriaId = 4)
    cate_producto_plantas = Producto.objects.filter(categoriaId = 5)
    return render(request,"catalogo.html",{"Producto":productos,"cate_flores":cate_producto_flores,"cate_herr":cate_producto_herramientas,
                                           "cate_arb":cate_producto_arboles,"cate_mac":cate_producto_maceteros,"cate_pl":cate_producto_plantas})


def cargarAgregarProd(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    return render(request,"agregarProducto.html",{"cate":categorias,"prod":productos})

def agregarProducto(request):

    v_categoria = Categoria.objects.get(id_categoria = request.POST['cmbCategoria'])

    #print("Agregar Productos",request.POST)
    v_sku = request.POST['txtSku']
    v_nombre = request.POST['txtnombre']
    v_precio = request.POST['txtprecio']
    v_stock = request.POST['txtStock']
    v_descripcion = request.POST['txtDescripcion']
    v_imagen = request.FILES['txtImagen']

    try:
        Producto.objects.create(sku_prod = v_sku, nombre_prod = v_nombre, precio_prod = v_precio, stock_prod = v_stock, descripcion_prod = v_descripcion, imagenUrl_prod = v_imagen, categoriaId = v_categoria)

    except IntegrityError:
        messages.error(request, 'El sku ya existe')
        return redirect('/agregarProducto')
    return redirect('/agregarProducto')

def cargarEditarProducto(request,sku):
    prod = Producto.objects.get(sku_prod = sku)
    categorias = Categoria.objects.all()
    return render(request,"editarProducto.html",{"prod":prod,"cate":categorias})


def editarProducto(request):
   
    v_categoria = Categoria.objects.get(id_categoria = request.POST['cmbCategoria'])

    v_sku = request.POST['txtSku']
    productoBD = Producto.objects.get(sku_prod = v_sku)
    v_nombre = request.POST['txtnombre']
    v_precio = request.POST['txtprecio']
    v_stock = request.POST['txtStock']
    v_descripcion = request.POST['txtDescripcion']
   
    try: 
        v_imagen = request.FILES['txtImagen']
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(productoBD.imagenUrl_prod))
        os.remove(ruta_imagen)
    except:
        v_imagen = productoBD.imagenUrl_prod


    productoBD.nombre_prod = v_nombre
    productoBD.precio_prod = v_precio
    productoBD.stock_prod = v_stock
    productoBD.descripcion_prod = v_descripcion
    productoBD.categoriaId = v_categoria
    productoBD.imagenUrl_prod = v_imagen
    

    productoBD.save()
   

    return redirect('/agregarProducto')

def eliminarProducto(request,codigo_producto):
    producto = Producto.objects.get(sku_prod = codigo_producto)
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(producto.imagenUrl_prod))
    os.remove(ruta_imagen)
    producto.delete()
    return redirect('/agregarProducto')




  #Codigo Inicio y registro
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'Inicio.html',{
        'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'Inicio.html',{
                'form': AuthenticationForm,
                'error': 'El usuario o la contraseña es incorrecta'
            })
        else:
            login(request, user)
            return redirect('home')

def signup(request):

    if request.method == 'GET':
        return render(request,"signup.html",{
        'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user) #cookies
                return redirect('home')
            except:
                return render(request,"signup.html",{
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
                })   
        return render(request,"signup.html",{
            'form': UserCreationForm,
            "error": 'Contraseñas no coinciden'
        })   


#@login_required
def obtenerProducto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigosProd = data.get('codigosProd',[])

        contador = defaultdict(int)

        for cod in codigosProd:
            contador[cod] += 1
        
        listaCod = list(set(codigosProd))

        productos = Producto.objects.filter(sku_prod__in=listaCod)

        almacenarDatos = []
        for producto in productos:
            sku = producto.sku_prod
            cantidad = contador[sku]
            almacenarDatos.append({
                'sku_prod': producto.sku_prod,
                'nombre_prod': producto.nombre_prod,
                'imagenUrl_prod': producto.imagenUrl_prod.url,
                'stock_prod': producto.stock_prod,
                'precio_prod': producto.precio_prod,
                'descripcion_prod': producto.descripcion_prod,
                'cantidad': cantidad 
            })
        return JsonResponse(almacenarDatos, safe=False)

    return JsonResponse({'error': 'error'}, status=405)

def actualizarStock(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigosProd = data.get('sku_prod')
        cantidad = data.get('cantidad')
        if codigosProd is not None and cantidad is not None:
            try:
                producto = Producto.objects.get(sku_prod=codigosProd)
                if(cantidad>producto.stock_prod):
                    cantidad = producto.stock_prod
                    producto.stock_prod -= int(cantidad) 
                    producto.save()  
                else:
                    producto.stock_prod -= int(cantidad)
                    producto.save()  
                
                    return JsonResponse({'status': 'OK'})
            except Producto.DoesNotExist:
                return JsonResponse({'message': 'Producto no encontrado'})
            
            except ValueError:
                return JsonResponse({'message': 'Error en cantidad del producto'})
        else:
            return JsonResponse({'message': 'Error'})

    return JsonResponse({'message': 'Error'})
#------------------------------------------------------------------------------------------------------------#
def iniciar_transaccion(request):
    if request.method == 'POST':
        totalCompra = request.POST.get('totalCompra')  # Obtener el valor de totalCompra en lugar de amount
        buy_order = 'ordenCompra12345678'
        session_id = 'sesion1234564'
        return_url = request.build_absolute_uri('/transbank/completar-transaccion/')

        response = Transaction().create(buy_order, session_id, totalCompra, return_url)  # Pasar totalCompra en lugar de amount

        if 'token' in response and 'url' in response:
            return redirect(response['url'] + '?token_ws=' + response['token'])
        else:
            return render(request, 'error.html', {'message': 'Error al iniciar la transacción.'})
    else:
        return redirect('mostrar_formulario')


def completar_transaccion(request):
    token = request.GET.get('token_ws')
    response = Transaction().commit(token)

    if 'response_code' in response and response['response_code'] == 0:
        return render(request, 'success.html', {'response': response})
    else:
        return render(request, 'error.html', {'message': 'Error al completar la transacción.'})