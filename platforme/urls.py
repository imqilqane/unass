from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add-students/<str:pk>/<str:num>', views.add_students, name="add_students"),
    path('formation/', views.formation, name="formation"),
    path('edit-formation/<str:pk>', views.edit_formation, name="edit_formation"),
    path('formation/<str:pk>', views.formation_details, name="formation_details"),
    path('accept-formation/<str:pk>', views.accpet_invetation, name="accept_formation"),
    path('refuse-formation/<str:pk>', views.refuse_invetation, name="refuse_formation"),
]
