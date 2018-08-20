from django.urls import path
from . import views

urlpatterns = [
    path('delete/', views.delete, name='delete_reservation'),
    path('<int:reservation_id>', views.view_reservation, name='view_reservation'),
]
