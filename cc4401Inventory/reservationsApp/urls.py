from django.urls import path
from . import views

urlpatterns = [
    path('delete/', views.delete, name='delete_reservation'),
    path('<int:reservation_id>', views.article_reservation_data, name='view_reservation'),
]
