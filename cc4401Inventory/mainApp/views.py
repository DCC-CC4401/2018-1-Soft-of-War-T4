from django.shortcuts import render
from django.utils.timezone import localtime
import datetime
from mainApp.models import User
from articlesApp.models import Article
from reservationsApp.models import Space_Reservation
from spacesApp.models import Space
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def landing_articles(request):
        context = {}
        return render(request, 'articulos.html', context)


@login_required
def landing_spaces(request, date=None):

    if date:
        current_date = date
        current_week = datetime.datetime.strptime(current_date,"%Y-%m-%d").date().isocalendar()[1]
        current_year = datetime.datetime.strptime(current_date,"%Y-%m-%d").date().isocalendar()[0]
    else:
        try:
            current_week = datetime.datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
            current_year = datetime.datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[0]
            current_date = request.GET["date"]
        except:
            current_week = datetime.date.today().isocalendar()[1]
            current_year = datetime.date.today().isocalendar()[0]
            current_date = datetime.date.today().strftime("%Y-%m-%d")

    reservations = Space_Reservation.objects.filter(starting_date_time__week = current_week,starting_date_time__year = current_year, state__in = ['P','A'])
    colores = {'A': 'rgba(0,153,0,0.7)',
               'P': 'rgba(51,51,204,0.7)'}

    res_list = []
    for i in range(5):
        res_list.append(list())
    for r in reservations:
        reserv = []
        reserv.append(r.space.name)
        reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
        reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
        reserv.append(colores[r.state])
        reserv.append(r.space.id)
        res_list[r.starting_date_time.isocalendar()[2]-1].append(reserv)

    move_controls = list()
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=-4)).strftime("%Y-%m-%d"))
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=-1)).strftime("%Y-%m-%d"))
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=4)).strftime("%Y-%m-%d"))

    delta = (datetime.datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2])-1
    monday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%d/%m/%Y"))

    if request.method == 'POST':
        try:
            dia_reserva = int(request.POST['day'])
            error = False

            if dia_reserva < 0 or dia_reserva > 4:
                raise ValueError

            espacio_str = request.POST['espacio_reservado']
            hora_ini_str = request.POST['reserv_ini'].split(":")
            hora_fin_str = request.POST['reserv_fin'].split(":")

            hora_ini_num = int(hora_ini_str[0])*60 + int(hora_ini_str[1])
            hora_fin_num = int(hora_fin_str[0])*60 + int(hora_fin_str[1])

            if hora_ini_num >= hora_fin_num:
                messages.warning(request, 'La hora inicial debe ser después que la hora final.')
                error = True

            splited_monday = monday.split("/")
            fecha_ini_str = str(int(splited_monday[0]) + dia_reserva) + "-" + splited_monday[1] + "-" + splited_monday[2] + " " + ":".join(hora_ini_str)
            fecha_fin_str = str(int(splited_monday[0]) + dia_reserva) + "-" + splited_monday[1] + "-" + splited_monday[2] + " " + ":".join(hora_fin_str)

            fecha_ini = datetime.datetime.strptime(fecha_ini_str, '%d-%m-%Y %H:%M')
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%d-%m-%Y %H:%M')

            if fecha_ini < datetime.datetime.now() + datetime.timedelta(hours=24) and espacio_str == "Quincho":
                messages.warning(request, 'Reserva rechazada, recuerda que los prestamos del Quincho caducan 24 horas antes de la fecha de inicio del préstamo.')
                error = True
            elif fecha_ini < datetime.datetime.now() + datetime.timedelta(hours=1):
                messages.warning(request, 'No se pueden hacer reservas en un horario menor a una hora a partir de la hora actual.')
                error = True

            if not request.user.enabled:
                messages.warning(request, "Debes estar habilitado para hacer reservas para hacer una reserva :/")
                error = True

            espacio = Space.objects.filter(name=espacio_str).get()

            reservas_del_dia_antes = Space_Reservation.objects.filter(starting_date_time__range=(fecha_ini, fecha_fin), state='A')
            reservas_del_dia_despues = Space_Reservation.objects.filter(ending_date_time__range=(fecha_ini, fecha_fin), state='A')

            if reservas_del_dia_antes or reservas_del_dia_despues:
                messages.warning(request, "Este espacio está ocupado en este itervalo de tiempo")
                error = True

            if not error:
                reserva = Space_Reservation(space=espacio, starting_date_time=fecha_ini, ending_date_time=fecha_fin,
                                    user=request.user)
                reserva.save()

        except:
            messages.warning(request, 'Formulario Incorrecto')

    all_spaces = Space.objects.all()
    context = {'reservations' : res_list,
               'current_date' : current_date,
               'controls' : move_controls,
               'actual_monday' : monday,
               'spaces' : all_spaces,
               'enable_filters': True
               }
    return render(request, 'espacios.html', context)


@login_required
def landing_search(request, products):
    if not products:
        return landing_articles(request)
    else:
        context = {'productos' : products,
                   'colores' : {'D': '#009900',
                                'R': '#ffcc00',
                                'P': '#3333cc',
                                'L': '#cc0000'}
                   }
        return render(request, 'articulos.html', context)


@login_required
def search(request):
    if request.method == "GET":
        query = request.GET['query']
        #a_type = "comportamiento_no_definido"
        a_state = "A" if (request.GET['estado'] == "A") else request.GET['estado']

        if not (a_state == "A"):
            articles = Article.objects.filter(state=a_state,name__icontains=query.lower())
        else:
            articles = Article.objects.filter(name__icontains=query.lower())

        products = None if (request.GET['query'] == "") else articles
        return landing_search(request, products)
