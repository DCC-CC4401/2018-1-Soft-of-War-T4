from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cc4401Inventory.spacesApp.models import Space
from cc4401Inventory.reservationsApp.models import Space_Reservation
from django.db import models
from datetime import datetime, timedelta
from django.contrib import messages



@login_required
def space_request(request):
    if request.method == 'POST':
        space = Space.objects.get(id = request.POST['space_id'])

        if request.user.enabled:
            try:
                string_inicio = request.POST['fecha_inicio'] + " " + request.POST['hora_inicio']
                start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
                string_fin = request.POST['fecha_fin'] + " " + request.POST['hora_fin']
                end_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')

                if start_date_time > end_date_time:
                    messages.warning(request, 'La reserva debe terminar después de iniciar.')
                elif start_date_time < datetime.now() + timedelta(hours=1):
                    messages.warning(request, 'Los pedidos deben ser hechos al menos con una hora de anticipación.')
                else:
                    reservation = Space_Reservation(space=space, starting_date_time=start_date_time, ending_date_time=end_date_time,
                                user=request.user)
                    reservation.save()
                    messages.success(request, 'Pedido realizado con éxito')
            except Exception as e:
                messages.warning(request, 'Ingrese una fecha y hora válida.')
        else:
            messages.warning(request, 'Usuario no habilitado para pedir reservas')

        return redirect('/space/' + str(space.id))
