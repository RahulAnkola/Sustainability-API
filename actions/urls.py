from django.urls import path
from . import views

urlpatterns = [
    path('actions/', views.action_list),
    path('actions/<int:id>/', views.action_detail),
]
