from django.shortcuts import redirect, render, reverse
from .models import (
    Deplomat,
    Formation,
    ChooseUsReasons,
    WhyChoosingUs,
    TeamMember,
    OurContactInfo,
    MessagesFromNewClients,
    Activite,
    UnassActivite,
    CaralogueFormation,
    AnetmentUnass,
    )
from docx import Document
from django.contrib.auth.decorators import login_required
from user.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from datetime import date
from platforme.pdfHandling.pdfEdit import printOnPDF
from datetime import datetime
import os

def home(request):
    reasons = ChooseUsReasons.objects.all()
    choose_us_qs = WhyChoosingUs.objects.all()
    team = TeamMember.objects.all()
    contact_info_qs = OurContactInfo.objects.all()
    message = MessagesFromNewClients.objects.all()
    activites_qs = UnassActivite.objects.all()
    catalogue_formation = CaralogueFormation.objects.all()
    anetment_unass = AnetmentUnass.objects.all()

    context = {
            "reasons": reasons,
            "team": team,
            "catalogue_formation":catalogue_formation,
            "anetment_unass":anetment_unass
        }

    if choose_us_qs.exists():
        choose_us = choose_us_qs[0]
        context.update({"choose_us": choose_us})

    if activites_qs.exists():
        activites = activites_qs[0]
        context.update({"activites": activites})

    if contact_info_qs.exists():
        contact_info = contact_info_qs[0]
        context.update({"contact_info": contact_info})

    if request.method == 'POST':
        fName = request.POST.get('fName')
        Email = request.POST.get('Email')
        Subject = request.POST.get('Subject')
        Message = request.POST.get('message')

        new_message = MessagesFromNewClients.objects.create(
            name=fName,
            email=Email,
            subject=Subject,
            message=Message
        )

        email_sub = "New Clients Wanna Contact Us"
        email_body = f"{fName} sent a message at {new_message.date}"
        email_message = EmailMessage(
            email_sub,
            email_body,
            "noreplay@stdojoservices.com",
            ["inbmltd@gmail.com", ]
        )
        email_message.send()

        messages.success(
            request, 'Thank You For Contacting Us Your Message Is Recived And We Will Get In Touch With Very Soon')
        return redirect('home')


    return render(request, "plateforme/home.html", context)


@login_required
def formation(request):
    if request.user.is_staff:
        formateurs = User.objects.filter(is_active = True)
        if request.method == "POST":
            fromDate = request.POST.get('fromDate')
            toDate = request.POST.get('toDate')
            fermateur = request.POST.get('formateur')
            message = request.POST.get('message')
            fermateurObj = User.objects.get(id=fermateur)

            formation = Formation.objects.create(
                president = request.user,
                fromDate = fromDate,
                toDate = toDate,
                teacher  = fermateurObj,
                message =  message,
            )
            message = EmailMessage(
                '[UNASS MAROC] Demande de formation',
                f"""Bonjour {fermateurObj.first_name}, {request.user.last_name} vous offrir une opportunité de faire une formation dans sa branche, pouvez-vous s'il vous plaît le vérifier et y répondre""",
                "contact@unass.ma",
                [fermateurObj.email, ]
            )
            message.send()
            messages.success(request, "formation créé avec succès")
            return redirect('profile')
        context = {"formateurs":formateurs}
        return render(request, "plateforme/formation_directeur.html", context)
    elif request.user.is_active:
        return redirect('profile')
   
   
@login_required(login_url='login')
def formation_details(request, pk):
    formation = get_object_or_404(Formation, id = pk)
    context = {}
    if request.user == formation.teacher or request.user == formation.president or request.user.is_director_national:
        deplomats = formation.deplomat.all()
        context = {
            'title': 'formation détails',
            'formation': formation,
            'deplomats': deplomats
        }
        if request.method == "POST":
            studentsNumber = request.POST.get("studentsNumber")
            redirect_url = reverse('add_students', kwargs={"pk":pk,"num":studentsNumber})
            return redirect(redirect_url)

        return render(request , 'plateforme/formation_details.html' , context)
    else :
        return redirect('profile')

@login_required
def accpet_invetation(request, pk):
    formation = get_object_or_404(Formation, id = pk)
    if formation.teacher == request.user :
        formation.accepted = True
        formation.save()
        message = EmailMessage(
                '[UNASS MAROC] Response a votre demande de formation',
                f"""Bonjour {formation.president.first_name}, le formateur {request.user.last_name} est accepte votre demande de formation""",
                "contact@unass.ma",
                [formation.president.email, ]
            )
        message.send()
        messages.success(request, "Merci!")
        return redirect('profile')
    else :
        return redirect('profile')

@login_required
def refuse_invetation(request, pk):
    formation = get_object_or_404(Formation, id = pk)
    if formation.teacher == request.user :
        formation.refused = True
        formation.save()
        message = EmailMessage(
                '[UNASS MAROC] Response a votre demande de formation',
                f"""Bonjour {formation.president.first_name}, le formateur {request.user.last_name} est refuse votre demande de formation""",
                "contact@unass.ma",
                [formation.president.email, ]
            )
        message.send()
        messages.success(request, "Merci!")
        return redirect('profile')
    else :
        return redirect('profile')

def edit_formation(request, pk):
    formation = get_object_or_404(Formation, id = pk)
    if request.user == formation.president:
        formateurs = User.objects.filter(is_active = True)
        if request.method == "POST":
            fromDate = request.POST.get('fromDate')
            toDate = request.POST.get('toDate')
            fermateur = request.POST.get('formateur')
            message = request.POST.get('message')
            fermateurObj = User.objects.get(id=fermateur)
            formation.fromDate = fromDate
            formation.toDate = toDate
            formation.teacher = fermateurObj
            formation.refused = False
            formation.save()
            message = EmailMessage(
                '[UNASS MAROC] Demande de formation ',
                f"""Bonjour {fermateurObj.first_name}, {request.user.last_name} vous offrir une opportunité de faire une formation dans sa branche, pouvez-vous s'il vous plaît le vérifier et y répondre""",
                "contact@unass.ma",
                [fermateurObj.email, ]
            )
            message.send()
            messages.success(request, "formation Édité avec succès")
            return redirect('profile')
        context = {"formateurs":formateurs, "formation":formation}
        return render(request, "plateforme/edit_formation.html", context)
    return redirect('profile')
    
        
@login_required
def add_students(request, pk, num):
    limit = int(num) + 1
    if int(num) > 12 :
        redirect_url = reverse('formation_details', kwargs={"pk":pk})
        messages.warning(request, "Pardon! la limite est de 12 bénéficiaires par fourmateur")
        return redirect(redirect_url)
    if int(num) < 2 :
        redirect_url = reverse('formation_details', kwargs={"pk":pk})
        messages.warning(request, "désolé tu devrais avoir au moins un bénéficiaires")
        return redirect(redirect_url)
    try :
        formation = get_object_or_404(Formation, id = pk)
        certs_dir = f"{os.getcwd()}\\media\\{formation.id}"
        try :
            os.mkdir(certs_dir)
        except:
            pass
        formation.cert_dir = f"media/{formation.id}"
        formation.save()
        if formation.teacher == request.user :
            if request.method == "POST":
                students = [
                    {
                        "name":request.POST.get(f'{n}'),
                        "cin":request.POST.get(f'{n}-cin'),
                        "birth_day":request.POST.get(f'{n}-bt'),
                        "birthPlace":request.POST.get(f'{n}-birthPlace'),
                        "phoneNumber":request.POST.get(f'{n}-phoneNumber'),
                        "formationPlace":request.POST.get(f'{n}-formationPlace'),
                    } for n in range(1, limit)
                    ]
                try:
                    os.mkdir(f"./media/{formation.id}")
                except:
                    print("-- mkdir error")
                for student in students:
                    date = student["birth_day"].split('-')
                    date.reverse()
                    date = '-'.join(date)
                    print('date ', date)
                    diplomat = Deplomat(
                        student_name = student["name"],
                        cin = student["cin"],
                        birth_date = student["birth_day"],
                        formation = formation,
                        phoneNumber = student["phoneNumber"],
                        formationPlace = student["formationPlace"],
                        )
                    diplomat.save()
                    printOnPDF(
                        student["name"], student["cin"], date, student["birthPlace"], student["formationPlace"], 
                        str(formation.fromDate.strftime("%d/%m/%Y")), str(formation.toDate.strftime("%d/%m/%Y")), student["formationPlace"],str(formation.toDate.strftime("%d/%m/%Y")) , diplomat.serial_num, student["cin"], formation.id
                        )
                messages.success(request, "Les bénéficiaires ajoutés avec succès")
                return redirect('profile')
            context = {'range': range(1, limit), 'formation':formation}
            return render(request, "plateforme/add_students.html", context)
        else :
                return redirect('profile')
    except:
        messages.warning(request, "Quelque chose s'est mal passé ! Veuillez réessayer plus tard")
        return redirect('home')