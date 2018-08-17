from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from spacesApp.models import Space
from django.db import models
from datetime import datetime, timedelta

import random, os
import pytz
from django.contrib import messages



@login_required
def space_data(request, space_id):
    try:
        space = Space.objects.get(id=space_id)




        context = {
            'space': space,
        }

        return render(request, 'space_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')

@login_required
def space_data_admin(request, space_id):
    if not request.user.is_staff:
        return redirect('/')
    else:
        try:
            space = Space.objects.get(id=space_id)
            context = {
                'space': space
            }
            return render(request, 'space_data_admin.html', context)
        except:
            return redirect('/')



@login_required
def space_edit_name(request, space_id):

    if request.method == "POST":
        a = Space.objects.get(id=space_id)
        a.name = request.POST["name"]
        a.save()
    return redirect('/space/'+str(space_id)+'/edit')


@login_required
def space_edit_image(request, space_id):

    if request.method == "POST":
        u_file = request.FILES["image"]
        extension = os.path.splitext(u_file.name)[1]
        a = Space.objects.get(id=space_id)
        a.image.save(str(space_id)+"_image"+extension, u_file)
        a.save()

    return redirect('/space/' + str(space_id) + '/edit')



@login_required
def space_edit_capacity(request, space_id):

    if request.method == "POST":
        c=request.POST["capacity"]
        if c!="":
            a = Space.objects.get(id=space_id)
            a.capacity = c
            a.save()
    return redirect('/space/'+str(space_id)+'/edit')



@login_required
def space_edit_description(request, space_id):
    if request.method == "POST":
        a = Space.objects.get(id=space_id)
        a.description = request.POST["description"]
        a.save()

    return redirect('/space/' + str(space_id) + '/edit')


