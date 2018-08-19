from django.shortcuts import render, redirect
from .models import Space_Reservation
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from articlesApp.models import Article
from loansApp.models import Article_Loan
from django.db import models
from datetime import datetime, timedelta
from reservationsApp.models import Article_Reservation

import random, os
import pytz
from django.contrib import messages


def delete(request):
    if request.method == 'POST':
        reservation_ids = request.POST.getlist('reservation')
        try:
            for reservation_id in reservation_ids:
                reservation = Space_Reservation.objects.get(id=reservation_id)
                if reservation.state == 'P':
                    reservation.delete()
        except:
            messages.warning(request, 'Ha ocurrido un error y la reserva no se ha eliminado')

        return redirect('user_data', user_id=request.user.id)


@login_required
def article_reservation_data(request, reservation_id):
    try:
        article = Article_Reservation.objects.get(id=reservation_id)

        last_loans = Article_Loan.objects.filter(article=article,
                                         ending_date_time__lt=datetime.now(tz=pytz.utc)
                                         ).order_by('-ending_date_time')[:10]

        loan_list = list()
        for loan in last_loans:

            starting_day = loan.starting_date_time.strftime("%d-%m-%Y")
            ending_day = loan.ending_date_time.strftime("%d-%m-%Y")
            starting_hour = loan.starting_date_time.strftime("%H:%M")
            ending_hour = loan.ending_date_time.strftime("%H:%M")

            if starting_day == ending_day:
                loan_list.append(starting_day+" "+starting_hour+" a "+ending_hour)
            else:
                loan_list.append(starting_day + ", " + starting_hour + " a " +ending_day + ", " +ending_hour)


        context = {
            'article': article,
            'last_loans': loan_list
        }

        return render(request, 'article_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')