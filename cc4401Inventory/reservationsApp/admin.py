from django.contrib import admin
from .models import Space_Reservation
from .models import Article_Reservation

# Register your models here.
admin.site.register(Space_Reservation)

admin.site.register(Article_Reservation)
