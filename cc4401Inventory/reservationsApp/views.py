from django.shortcuts import render, redirect
from .models import Space_Reservation
from .models import Article_Reservation
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from articlesApp.models import Article
from loansApp.models import Article_Loan
from django.db import models
from datetime import datetime, timedelta
from reservationsApp.models import Article_Reservation
from mainApp.models import User
import random, os
import pytz
from django.contrib import messages


def delete(request):
    if request.method == 'POST':
        reservation_ids = request.POST.getlist('reservation')
        try:
            for reservation_id in reservation_ids:
                reservation = Article_Reservation.objects.get(id=reservation_id)
                if reservation.state == 'P':
                    reservation.delete()
        except:
            messages.warning(request, 'Ha ocurrido un error y la reserva no se ha eliminado')

        return redirect('user_data', user_id=request.user.id)


@login_required
def view_reservation(request, reservation_id):

    reservation = Article_Reservation.objects.get(id=reservation_id)
    user =  reservation.user
    article= reservation.article

    context = {
        'reservation': reservation,
        'user': user,
        'article': article,
        'id' : reservation_id
    }

    return render(request, 'reservation_data.html', context)
