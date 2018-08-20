# Generated by Django 2.0.5 on 2018-08-20 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('image', models.ImageField(blank=True, upload_to='static/img/items', verbose_name='Imagen del articulo')),
                ('state', models.CharField(choices=[('D', 'Disponible'), ('P', 'En préstamo'), ('R', 'En reparación'), ('L', 'Perdido')], max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
