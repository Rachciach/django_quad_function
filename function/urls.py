from django.urls import path
from . import views
urlpatterns = [

    path('function', views.function, name="function"),
    path('history', views.history, name="history"),
    path('values', views.values, name="values"),
    path('', views.index, name="main")
]
