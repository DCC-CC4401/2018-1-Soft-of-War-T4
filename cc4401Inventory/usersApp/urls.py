from django.urls import path

from . import views

urlpatterns = [
    path('<int:user_id>/', views.user_data, name='user_data'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('login/submit/', views.login_submit, name='login_submit'),
    path('signup/submit/', views.signup_submit, name='signup_submit'),
    path('logout/', views.logout_view, name='logout'),
    path('loan/<int:loan_id>/', views.loan_data, name='loan_data'),
    path('lost_loan/<int:loan_id>/', views.lost_request, name='lost_request'),
]

