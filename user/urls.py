from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    
]


urlpatterns = [
    path('sign_up/' ,views.registerFormateure , name='sign_up'),
    path('login/' ,views.login, name='login'),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.Userupdate, name='editprofile'),
    path('acces-beneficiers/', views.accesBeneficiers, name='acces_beneficiers'),
]