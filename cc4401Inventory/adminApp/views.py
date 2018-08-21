from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from reservationsApp.models import Space_Reservation
from reservationsApp.models import Article_Reservation
from loansApp.models import Article_Loan
from articlesApp.models import Article
from spacesApp.models import Space
from mainApp.models import User
from datetime import datetime, timedelta, date
import pytz
from django.utils.timezone import localtime
from django.contrib import messages

@login_required
def user_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'user_panel.html', context)

@login_required
def items_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    articles = Article.objects.all()
    spaces = Space.objects.all()
    context = {
        'articles': articles,
        'spaces': spaces
    }
    return render(request, 'items_panel.html', context)

@login_required
def actions_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    try:
        current_week = datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
        current_date = request.GET["date"]
    except:
        current_date = date.today().strftime("%Y-%m-%d")
        current_week = date.today().isocalendar()[1]

    colores = {'A': 'rgba(0,153,0,0.7)',
               'P': 'rgba(51,51,204,0.7)',
                'R': 'rgba(153, 0, 0,0.7)'}

    reservations = Space_Reservation.objects.filter(state='P').order_by('starting_date_time')
    current_week_reservations = Space_Reservation.objects.filter(starting_date_time__week=current_week)
    actual_date = datetime.now(tz=pytz.utc)
    loans = Article_Loan.objects.all().order_by('starting_date_time')

    try:
        if request.method == "POST":
            if request.POST["filter"]=='vigentes':
                loans = Article_Loan.objects.filter(state='V').order_by('starting_date_time')
            elif request.POST["filter"]=='caducados':
                loans = Article_Loan.objects.filter(state='C').order_by('starting_date_time')
            elif request.POST["filter"]=='perdidos':
                loans = Article_Loan.objects.filter(state='P').order_by('starting_date_time')
            else:
                loans = Article_Loan.objects.all().order_by('starting_date_time')
    except:
        loans = Article_Loan.objects.all().order_by('starting_date_time')

    res_list = []
    for i in range(5):
        res_list.append(list())
    for r in current_week_reservations:
        reserv = list()
        reserv.append(r.space.name)
        reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
        reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
        reserv.append(colores[r.state])
        reserv.append(r.space.id)
        res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)

    move_controls = list()
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=-4)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=-1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=4)).strftime("%Y-%m-%d"))

    delta = (datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2]) - 1
    monday = (
        (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=delta)).strftime("%d/%m/%Y"))

    all_spaces = Space.objects.all()
    context = {
        'reservations_query': reservations,
        'loans': loans,
        'reservations': res_list,
        'current_date': current_date,
        'controls': move_controls,
        'actual_monday': monday,
        'spaces' : all_spaces
    }
    return render(request, 'actions_panel.html', context)


def modify_reservations(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    if request.method == "POST":
        accept = True if (request.POST["accept"] == "1") else False
        try:

            reservations = Space_Reservation.objects.filter(id__in=request.POST["selected"])
            if accept:
                for reservation in reservations:
                    reservation.state = 'A'
                    reservation.save()
                    accept = Article_Loan(user=reservation.user,
                                      space=reservation.article,
                                      starting_date_time=reservation.starting_date_time,
                                        ending_date_time=reservation.ending_date_time)
                    accept.save()
            else:
                for reservation in reservations:
                    reservation.state = 'R'
                    reservation.save()
            return redirect('/admin/actions-panel')
        except:
            messages.warning(request, 'No se seleccionaron Reservas')
            return redirect('/admin/actions-panel')


def modify_loans(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    if request.method == "POST":

        accept = True if (request.POST["recibir"] == "1") else False
        try:
            loans = Article_Loan.objects.filter(id__in=request.POST["selected"])
            if accept:
                for loan in loans:
                    loan.state = 'R'
                    loan.save()
            else:
                for loan in loans:
                    loan.state = 'P'
                    loan.save()

            return redirect('/admin/actions-panel')

        except:
            messages.warning(request, 'No se seleccionaron Prestamos')
            return redirect('/admin/actions-panel')
