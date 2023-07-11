from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.template import loader 
from .models import Korisnik,Predmeti,Upisi
from .forms import AddUserForm,AddSubjectForm
from django import forms 


# Create your views here.

def logged_in(request):
    return render(request, 'profile.html')

def check_logged_in_user(request):
    korisnikId = request.user.pk
    loggeduser = Korisnik.objects.get(id=korisnikId)

    if loggeduser.role == 'admn':
        return redirect('adminpage')
    elif loggeduser.role == 'prof':
        return redirect('professorpage')
    else:
        return redirect('studentpage')

def custom_logout(request):
    return render(request, 'home.html')
     
def professor_page(request):
    return render(request, 'professorpage.html')

def student_page(request):
    return render(request, 'studentpage.html')

def admin_page(request):
    return render(request, 'adminpage.html')

def professors(request):
    profesori = Korisnik.objects.all().filter(role='prof')
    return render(request, 'professors.html', {'profesori': profesori})

def subjects(request):
    subjects = Predmeti.objects.all()
    return render(request, 'subjects.html', {'subjects': subjects})

def students(request):
    students = Korisnik.objects.all().filter(role='stu')
    return render(request, 'students.html', {'students': students})

def add_professor(request):
    if request.method == "GET":
        form = AddUserForm(initial={'role': 'prof', 'status': 'none'})
        form.fields['status'].widget = forms.HiddenInput()
        form.fields['role'].widget = forms.HiddenInput()
        return render(request, 'add_profesor.html', {'form': form})
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        form.fields['status'].widget = forms.HiddenInput()
        form.fields['role'].widget = forms.HiddenInput()
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'prof'
            user.save()
            return redirect('adminpage')
        else:
            return render(request, 'add_profesor.html', {'form': form})

def add_student(request):
    if request.method == "GET":
        form = AddUserForm(initial={'role': 'stu', 'status': 'none'})
        form.fields['role'].widget = forms.HiddenInput()
        return render(request, 'add_profesor.html', {'form': form})
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        form.fields['role'].widget = forms.HiddenInput()
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'stu'
            user.save()
            return redirect('students')
        else:
            return render(request, 'add_profesor.html', {'form': form})

def add_subject(request):
    if request.method == "GET":
        forma = AddSubjectForm()
        return render(request, 'add_profesor.html', {'form': forma})
    elif request.method == "POST":
        forma = AddSubjectForm(request.POST)
        if forma.is_valid():
            forma.save()
            return redirect('subjects')
    return render(request, 'add_profesor.html', {'form': forma})


def subject_details(request,subjectId):
    subject = Predmeti.objects.get(pk=subjectId)
    upisi = Upisi.objects.all().filter(predmet=subjectId)
    upisaniStudenti = Upisi.objects.all().filter(predmet=subject, status='upisan')

    if request.method == "POST":
        for item in upisaniStudenti:
            if item.korisnik.username in request.POST:
                student = Korisnik.objects.get(username=item.korisnik.username)
                if request.POST[item.korisnik.username] == 'pol': 
                    upisni = Upisi.objects.filter(korisnik=student, predmet=subject)
                    upisni.update(status="polozen", predmet=subject,korisnik=student)
                else:
                    upisni = Upisi.objects.filter(korisnik=student, predmet=subject)
                    upisni.update(status="izgubljenPotpis", predmet=subject,korisnik=student)

    return render(request,'subjectDetails.html', {'subject':subject,"upisi":upisi})

def edit_subjects(request,subjectId):
    subject = Predmeti.objects.get(pk=subjectId)

    if request.method == "GET":
        thisform = AddSubjectForm(instance=subject)
        return render(request, 'editsubject.html', {'form': thisform})
    elif "update" in request.POST:
        thisform = AddSubjectForm(request.POST, instance=subject)
        if thisform.is_valid():
            thisform.save()
            return redirect('subjects')
    else:
        subject.delete()
        return redirect('subjects')


def edit_students(request,studentId):
    user = Korisnik.objects.get(pk=studentId)
    thisform = AddUserForm(instance=user)

    if request.method == "GET":
        thisform = AddUserForm(instance=user)
        thisform.fields['role'].widget = forms.HiddenInput()
        return render(request, 'editsubject.html', {'form': thisform})
    elif "update" in request.POST:
        thisform = AddUserForm(request.POST, instance=user)
        if thisform.is_valid():
            thisform.fields['role'].widget = forms.HiddenInput()
            thisform.save()
            return redirect('students')
    else:
        user.delete()
        return redirect('students')


def edit_profesor(request,profId):
    user = Korisnik.objects.get(pk=profId)
    thisform = AddUserForm(instance=user)

    if request.method == "GET":
        thisform = AddUserForm(instance=user)
        thisform.fields['status'].widget = forms.HiddenInput()
        return render(request, 'editsubject.html', {'form': thisform})
    elif "update" in request.POST:
        thisform = AddUserForm(request.POST, instance=user)
        if thisform.is_valid():
            thisform.fields['status'].widget = forms.HiddenInput()
            thisform.save()
            return redirect('professors')
    else:
        user.delete()
        return redirect('professors')


def upisni_list(request,studentID):
    student = Korisnik.objects.get(pk=studentID)
    subjects = Predmeti.objects.all()
    upisni_list = Upisi.objects.all()
    sem = {1:"Prvi Sem",2:"Drugi Sem",3:"Treci Sem",4:"Cetvrti Sem",5:"Peti Sem",6:"Sesti Sem"}
    
    

    if request.method == "POST":
        for predmet in subjects:
            ul = Upisi.objects.filter(korisnik=student, predmet=predmet)
            if predmet.name in request.POST:
                if request.POST[predmet.name] == '+': 
                    if ul:
                        ul.update(status="upisan", korisnik=student, predmet=predmet)
                    else:
                        ul = Upisi(status="upisan", korisnik=student, predmet=predmet)
                        ul.save()
                elif request.POST[predmet.name] == 'pol':
                    ul.update(status="polozen", korisnik=student, predmet=predmet)
                elif request.POST[predmet.name] == 'x':
                    ul.delete()
    
    return render(request, 'upisniliststudent.html', {'subject': subjects,"upisnilist": upisni_list, "student":student,"sem":sem,})

def professor_subjects(request):
    predmeti = Predmeti.objects.all().filter(nositelj=request.user.pk)

    return render(request,"mysubjects.html",{"predmeti":predmeti})

def obrana(request):
    subjects = Predmeti.objects.all()
    x = []
    polozeni = Upisi.objects.all()
    

    for p in subjects:
        redovniBroj = len(polozeni.filter(predmet=p, korisnik__status="red", status='polozen'))
        vanredniBroj = len(polozeni.filter(predmet=p, korisnik__status="izv", status='polozen'))
        ukupno = redovniBroj+vanredniBroj
        x.append({"ImePredmeta":p.name,"UkupnoRed":redovniBroj,"UkupnoVanred":vanredniBroj,"SveSkupa":ukupno,"id":p.pk})

    return render(request, "obrana.html",{"upisni":subjects,"dict":x}) 

def obranazad2(request,pk):
    upisni = Predmeti.objects.all().filter(pk=pk)
    upisnisvi = Predmeti.objects.all()
    x = []


    for u in upisnisvi:
        if upisni.name == u.predmet["name"]:
            x.append({"ImeStudenta":u.korisnik.username,"StatusStudenta": u.korisnik.status})

    return render(request, "obrana2.html",{"upisni":x}) 



    
