from django.db import models

# Create your models here.

class Rol(models.Model):
    id_rol = models.IntegerField(primary_key=True)
    nombre_rol = models.CharField(max_length=15)

    def __str__(self):
        txt = "{0} - {1}"
        return txt.format(self.id_rol, self.nombre_rol)
 

class Usuario(models.Model):
    id_user = models.IntegerField(primary_key=True)
    nombre_user = models.CharField(max_length=50)   
    correo_user = models.EmailField()
    fecha_nacimiento_user = models.DateField()
    telefono_user = models.IntegerField() 
    contraseña_user = models.CharField(max_length=10)
    suscrito_user = models.BooleanField()


    def __str__(self):
        txt = "{0} - {1} - {6}"
        return txt.format(self.id_user, self.nombre_user, self.suscrito_user)




class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True)
    nombre_categoria = models.CharField(max_length=22)

    def __str__(self):
        txt = "{0} - {1}"
        return txt.format(self.id_categoria , self.nombre_categoria)


class Producto(models.Model):
    sku_prod = models.CharField(primary_key=True,max_length=15)
    nombre_prod = models.CharField(max_length=50)
    precio_prod = models.IntegerField()
    stock_prod = models.IntegerField()
    fecha_prod = models.DateField(auto_now_add=True)
    descripcion_prod = models.CharField(max_length=120)
    imagenUrl_prod = models.ImageField(upload_to="imagenesProducto")
    categoriaId = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        txt = "Producto N° {0} - Stock {1} - Precio {2} - fecha {3}"
        return txt.format(self.sku_prod, self.stock_prod, self.precio_prod,self.fecha_prod)