# Generated by Django 2.0.5 on 2018-08-16 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articlesApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='capacity',
            field=models.PositiveIntegerField(default=0, verbose_name='Capacidad'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/img/items', verbose_name='Imagen del articulo'),
        ),
    ]
