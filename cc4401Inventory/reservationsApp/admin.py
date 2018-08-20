from django.contrib import admin
from .models import Space_Reservation, Article_Reservation


# Register your models here.
admin.site.register(Article_Reservation)
admin.site.register(Space_Reservation)
