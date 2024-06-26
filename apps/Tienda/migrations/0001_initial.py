# Generated by Django 4.2.1 on 2023-06-09 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_categoria', models.CharField(max_length=22)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_user', models.IntegerField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_user', models.CharField(max_length=50)),
                ('correo_user', models.EmailField(max_length=254)),
                ('fecha_nacimiento_user', models.DateField()),
                ('telefono_user', models.IntegerField(max_length=11)),
                ('contraseña_user', models.CharField(max_length=10)),
                ('suscrito_user', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('sku_prod', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('nombre_prod', models.CharField(max_length=50)),
                ('precio_prod', models.IntegerField()),
                ('stock_prod', models.IntegerField()),
                ('fecha_prod', models.DateField(auto_now_add=True)),
                ('descripcion_prod', models.CharField(max_length=120)),
                ('imagenUrl_prod', models.CharField(max_length=200)),
                ('categoriaId_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tienda.categoria')),
            ],
        ),
    ]
