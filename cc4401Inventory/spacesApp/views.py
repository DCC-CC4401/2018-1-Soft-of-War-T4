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



