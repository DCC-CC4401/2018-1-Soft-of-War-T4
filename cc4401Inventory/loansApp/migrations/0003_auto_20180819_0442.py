# Generated by Django 2.0.5 on 2018-08-19 04:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articlesApp', '0002_auto_20180819_0442'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loansApp', '0002_loan_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article_Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_date_time', models.DateTimeField()),
                ('ending_date_time', models.DateTimeField()),
                ('state', models.CharField(choices=[('V', 'Vigente'), ('C', 'Caducado'), ('P', 'Perdido')], default='V', max_length=1, verbose_name='Estado')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articlesApp.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='loan',
            name='article',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='user',
        ),
        migrations.DeleteModel(
            name='Loan',
        ),
    ]
