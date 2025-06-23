from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
]
