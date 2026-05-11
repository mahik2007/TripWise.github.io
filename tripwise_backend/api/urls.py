from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('create-group/', views.create_group),
    path('add-expense/', views.add_expense),
    path('balances/<int:group_id>/', views.balances),
    path('settle/<int:group_id>/', views.settle_up),
    path('chatbot/', views.chatbot),
]