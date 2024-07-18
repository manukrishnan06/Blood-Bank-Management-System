from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect ,get_object_or_404
from donorandpatient.models import donorregisterdb, userregisterdb, makerequestdb, donateblooddb

def homepagefn(request):
    return render(request, "homepage.html")

def patientloginfn(request):
    return render(request, "patientlogin.html")

def patientloginfnn(request):
    if request.method == "POST":
        un = request.POST.get('uname')
        pwd = request.POST.get('upass')
        if userregisterdb.objects.filter(username=un, password=pwd).exists():
            request.session['username'] = un
            request.session['password'] = pwd
            return redirect(patienthomePagefn)
        else:
            return redirect(patientloginfn)
    else:
        return redirect(patientloginfn)

def donorloginfn(request):
    return render(request, "donorlogin.html")

def donorloginfnn(request):
    if request.method == "POST":
        un = request.POST.get('uname')
        pwd = request.POST.get('upass')
        if donorregisterdb.objects.filter(username=un, password=pwd).exists():
            request.session['username'] = un
            request.session['password'] = pwd
            return redirect('donorhomePagefn')
        else:
            return redirect('donorloginfn')
    else:
        return redirect('donorloginfn')

def patienthomePagefn(request):
    data = makerequestdb.objects.filter(patientname=request.session.get('username', ''))
    x = data.count()
    return render(request, "patientpage.html", {'data': data, 'x': x})

def donorhomePagefn(request):
    return render(request, "donorpage.html")

def pateientregfn(request):
    return render(request, "patientregistration.html")

def patienthistory(request):
    username = request.session.get('username', '')
    print(f"Session Username: {username}")  # Debug: Print username to console
    data = makerequestdb.objects.filter(patientname=username)
    print(data)  # Debug: Print data to console
    return render(request, "patientrequesthistory.html", {'data': data})


def savepatientregfn(request):
    if request.method == "POST":
        a = request.POST.get('pusern')
        c = request.POST.get('ppass')
        d = request.POST.get('pcpass')
        e = request.POST.get('page')
        f = request.POST.get('pblood')
        g = request.POST.get('pdis')
        h = request.POST.get('paddress')
        i = request.POST.get('pcontact')
        img = request.FILES.get('pimage')
        obj = userregisterdb(username=a, password=c, confirmpassword=d, age=e, bloodgroup=f, disease=g, address=h, contact=i, photo=img)
        obj.save()
        return redirect('patientloginfn')

def donorregfn(request):
    return render(request, "donorregister.html")

def savedonorregfn(request):
    if request.method == "POST":
        usern = request.POST.get('dusern')
        passs = request.POST.get('dpass')
        cpass = request.POST.get('dcpass')
        agee = request.POST.get('dage')
        blood = request.POST.get('dblood')
        addressp = request.POST.get('daddress')
        contactp = request.POST.get('dcontact')
        imge = request.FILES.get('dimage')
        obj = donorregisterdb(username=usern, password=passs, confirmpassword=cpass, age=agee, bloodgroup=blood, address=addressp, contact=contactp, photo=imge)
        obj.save()
        return redirect('donorloginfn')

def patientrequest(request):
    return render(request, "patientmakerequest.html")

def saverequest(request):
    if request.method == "POST":
        name = request.POST.get('pname')
        age = request.POST.get('page')
        rea = request.POST.get('preason')
        blood = request.POST.get('pblood')
        uni = request.POST.get('punit')
        obj = makerequestdb(patientname=name, patientage=age, reason=rea, bloodgroup=blood, unit=uni)
        obj.save()
        return redirect('patienthomePagefn')



def donateBloodfn(request):
    return render(request, "donateblood.html")

def savedonatebloodfn(request):
    if request.method == "POST":
        name = request.POST.get('dname')
        age = request.POST.get('dage')
        dis = request.POST.get('ddis')
        blood = request.POST.get('dblood')
        uni = request.POST.get('dunit')
        obj = donateblooddb(donorname=name, donorage=age, disease=dis, bloodgroup=blood, unit=uni)
        obj.save()
        return redirect('donorhomePagefn')

def donationhistoryfn(request):
    data = donateblooddb.objects.filter(donorname=request.session.get('username', ''))
    return render(request, "donationhistory.html", {'data': data})

from django.shortcuts import render, get_object_or_404
from .models import donorregisterdb

def donormyprofile(request):
    username = request.session.get('username', '')

    try:
        donor = donorregisterdb.objects.filter(username=username).first()
        if not donor:
            raise donorregisterdb.DoesNotExist("Donor does not exist")
    except donorregisterdb.DoesNotExist as e:
        # Handle the case where no donor with the given username is found
        print(f"Error: {e}")
        return render(request, 'error_page.html')  # Render an error page or handle gracefully

    context = {
        'd': donor
    }
    return render(request, 'donormyprofile.html', context)



def donoreditprofile(request):
    username = request.user.username  # Assuming the username is the same as the logged-in user

    donor = get_object_or_404(donorregisterdb, username=username)

    if request.method == 'POST':
        # Retrieve form data
        bloodgroup = request.POST.get('bloodgroup')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        photo = request.FILES.get('photo')

        # Validation
        if not bloodgroup or not contact or not address:
            return render(request, 'edit_profile.html', {
                'd': donor,
                'error': 'All fields except photo are required.'
            })

        # Update donor object
        donor.bloodgroup = bloodgroup
        donor.contact = contact
        donor.address = address
        if photo:
            donor.photo = photo

        # Save donor object
        donor.save()

        # Redirect to profile page after successful update
        return redirect('donormyprofile')

    # If request method is not POST, render the edit profile form
    context = {
        'd': donor,
    }
    return render(request, 'donoreditprofile.html', context)


def patientLogout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('patientloginfn')


def donorLogout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('donorloginfn')
