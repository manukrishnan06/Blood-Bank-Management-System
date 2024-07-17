from django.shortcuts import render,redirect
from blood.models import Donordb
from donorandpatient.models import userregisterdb, donorregisterdb, donateblooddb, makerequestdb
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage

# Create your views here.


def indexfn(request):
    x=0
    A=0
    B=0
    C=0
    D=0
    E=0
    F=0
    G=0
    data=donateblooddb.objects.all()
    blood=makerequestdb.objects.all()

    for d in data:
        if d.bloodgroup=="A+":
            x=x+d.unit
        if d.bloodgroup=="B+":
            A=A+d.unit
        if d.bloodgroup=="O+":
            B=B+d.unit
        if d.bloodgroup=="AB+":
            C=C+d.unit
        if d.bloodgroup=="A-":
            D=D+d.unit
        if d.bloodgroup=="B-":
            E=E+d.unit
        if d.bloodgroup=="O-":
            F = F + d.unit
        if d.bloodgroup=="AB-":
            G = G + d.unit
    for b in blood:
        if b.bloodgroup=="A+":
            x=x-b.unit
        if b.bloodgroup == "B+":
            A = A-b.unit
        if b.bloodgroup == "B+":
            B = B - b.unit
        if b.bloodgroup == "B+":
            C = C - b.unit
        if b.bloodgroup == "B+":
            D = D - b.unit
        if b.bloodgroup == "B+":
            E = E - b.unit
        if b.bloodgroup == "B+":
            F = F - b.unit
        if b.bloodgroup == "B+":
            G = G - b.unit


    return render(request,"index.html" ,{'data':data,'x':x,'A':A,'B':B,'C':C,'D':D,'E':E,'F':F,'G':G,'blood':blood})

def donorfn(request):
    return render(request,"donor.html")

def davedonorfn(request):
    if request.method == "POST":
        a = request.POST.get('pname')
        b = request.FILES['image']
        c = request.POST.get('pblood')
        d = request.POST.get('paddress')
        e = request.POST.get('pcontact')
        obj = Donordb(Name=a,Photo=b,Bloodgroup=c,Address=d,Contact=e)
        obj.save()
        return redirect(donorfn)

def displaydonorfn(request):
    data =donorregisterdb.objects.all()
    return render(request,"donordisplay.html",{'data':data})


def displaypatientfn(request):
    data = userregisterdb.objects.all()
    return render(request,"patientdisplay.html",{'data':data})


def editpatientfn(request,pid):
    data = userregisterdb.objects.get(id=pid)
    return render(request,"patientedit.html",{'data':data})


def updatepatientfn(request,pid):
    if request.method == "POST":
        h = request.POST.get('pname')
        i = request.POST.get('pblood')
        j = request.POST.get('page')
        k = request.POST.get('pdis')
        l = request.POST.get('pcontact')

        try:
            im = request.FILES['pimage']
            fs = FileSystemStorage()
            file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            file = userregisterdb.objects.get(id=pid).photo

    userregisterdb.objects.filter(id=pid).update(name=h,bloodgroup=i,age=j,disease=k,contact=l,photo=file)
    return redirect(displaypatientfn)


def editdonorfn(request,did):
    data = donorregisterdb.objects.get(id=did)
    return render(request,"donoredit.html",{'data':data})


def updatedonorfn(request,did):
    if request.method == "POST":
        a = request.POST.get('dname')
        b = request.POST.get('dblood')
        c = request.POST.get('dage')
        d = request.POST.get('daddress')
        e = request.POST.get('dcontact')

        try:
            im = request.FILES['dimage']
            fs = FileSystemStorage()
            file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            file = donorregisterdb.objects.get(id=did).photo

    userregisterdb.objects.filter(id=did).update(name=a,bloodgroup=b,age=c,address=d,contact=e,photo=file)
    return redirect(displaydonorfn)


def displaydonations(request):
    data =donateblooddb.objects.all()
    return render(request,"Donations.html",{'data':data})


def displaybloodRequests(request):
    data =makerequestdb.objects.all()
    return render(request,"bloodrequest.html",{'data':data})


def approverequest(request,sid):
    data = donateblooddb.objects.get(id=sid)
    return render(request,"approverequest.html",{'data':data})

def deletedonorfn(request, did):
    donor = donorregisterdb.objects.get(id=did)
    donor.delete()
    return redirect(displaydonorfn)
