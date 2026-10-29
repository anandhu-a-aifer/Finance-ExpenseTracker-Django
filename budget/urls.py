from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("transactions/add/",views.add_transaction,name="add_transaction",),
    path("transactions/<int:pk>/delete/",views.delete_transaction,name="delete_transaction",),
    path("register/", views.register, name="register"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/<int:pk>/edit/", views.edit_category, name="edit_category"),
    path("categories/<int:pk>/delete/", views.delete_category, name="delete_category"),
]