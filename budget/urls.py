from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("transactions/add/",views.add_transaction,name="add_transaction",),
    path("transactions/<int:pk>/delete/",views.delete_transaction,name="delete_transaction",),
    path("register/", views.register, name="register"),
]