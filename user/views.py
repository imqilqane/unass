from django.shortcuts import render, redirect
from .models import User
from platforme.models import Deplomat
from django.contrib.auth import authenticate, logout
from django.contrib.auth import  login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import exceptions
from platforme.models import Formation
from .forms import Userupdateform, Proupdateform
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from datetime import timedelta
from platforme.models import AnetmentUnass
import json

def registerFormateure(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email') 
        password = request.POST.get('password1') 

        if len(User.objects.filter(email=email)) > 0:
            messages.warning(request, "Cet e-mail est déjà pris")
            return redirect('sign_up')

        if len(User.objects.filter(username=username)) > 0:
            messages.warning(request, "Cet nom d'utilisateur est déjà pris")
            return redirect('sign_up')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.is_active = False
        user.save()
        messages.success(request, "vous vous êtes inscrit avec succès, nous examinerons votre demande et si vous êtes l'un de nos Formateure, nous vous accepterons")
        return redirect('home')
    return render (request,'user/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        try :
            user = User.objects.get(email=email)
            if user.check_password(password):
                if not user.is_active:
                    messages.warning(request, "ce compte est toujours en cours d'examen")
                    return redirect('login')
                auth_login(request , user)
                messages.success(request, "Vous vous êtes connecté avec succès")
                return redirect('profile')
            else :
                messages.warning(request, "le mot de passe est uncorrect")
        except exceptions.ObjectDoesNotExist:
            messages.warning(request, "il n'y a aucun utilisateur correspondant à cet email")
        except :
            messages.warning(request, "something went wrong! please try again later")
        return redirect('login')

    return render (request,'user/login.html')

def accesBeneficiers(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        cin = request.POST.get('cin')
        Deplomat_qs = Deplomat.objects.filter(cin=cin)
        if Deplomat_qs.exists():
            context.update({
                'Deplomat':Deplomat_qs[len(Deplomat_qs) -1],
                'renewal' : Deplomat_qs[len(Deplomat_qs) -1].formation.toDate + timedelta(days=365)
                })
        else :
            messages.warning(request, "Désolé ce CIN est introuvable!")
            return redirect('acces_beneficiers')

    return render (request,'user/access_beneficier.html', context)

def filterFormation(antenneId):
    if antenneId:
        antenne = AnetmentUnass.objects.get(id=antenneId)
        formations = Formation.objects.filter(antenne=antenne)
        return formations
    return Formation.objects.all()

@login_required(login_url='login')
def profile (request):
    user = request.user
    antennes = AnetmentUnass.objects.all()
    context = {
        'title': 'profile',
        'user':user,
        'antennes':antennes
    }
    body_unicode = request.body.decode('utf-8')
    antenneId =  body_unicode[-1] if body_unicode else None
    print("body_unicode => ",body_unicode)
    formations = None
    if request.user.is_director_national:
        formations = filterFormation(antenneId)
        staff_as_formateaur_formations = Formation.objects.filter(teacher=request.user)
        context["staff_as_formateaur_formations"] = staff_as_formateaur_formations
    elif request.user.is_staff: 
        formations = filterFormation(antenneId)
        staff_as_formateaur_formations = Formation.objects.filter(teacher=request.user)
        context["staff_as_formateaur_formations"] = staff_as_formateaur_formations
    else:
        formations = filterFormation(antenneId)

    paginator = Paginator(formations,10)
    page =request.GET.get('page')
    try:
        formations = paginator.page(page)
    except PageNotAnInteger :
        formations = paginator.page(1)
    except EmptyPage :
        formations = paginator.page(paginator.num_pages)
    context["formations"] = formations
    return render(request,'user/profile.html' , context)



@login_required(login_url='login')
def Userupdate( request):
    if request.method == 'POST':
            user_form = Userupdateform(request.POST , instance=request.user)
            pro_form = Proupdateform(request.POST , request.FILES, instance=request.user.user_profile) #hitax had l7a9l kay3dal ta lmilafat
            if user_form.is_valid() and pro_form.is_valid():
                user_form.save()
                pro_form.save()
                messages.success(request,  ' Vous avez mis à jour votre profil avec succès ')
                return redirect('profile')
    else:
            user_form = Userupdateform(instance=request.user)
            pro_form = Proupdateform(instance=request.user.user_profile)
    context = {
        'title' : 'Edit profile ' ,
        'user_form' : user_form,
        'pro_form' : pro_form,
    }
    return render(request , 'user/userupdate.html' , context)
