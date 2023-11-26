from django.shortcuts import render
from .models import Destination
from .models import Detailed_desc
from .models import pessanger_detail
from .models import Cards
from .models import Transactions
from .models import NetBanking,Suggestion
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.utils.dateparse import parse_date
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.template import Library
from datetime import datetime
from django.contrib.auth.models import User
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404
from .models import Destination
from .forms import CountryForm 
from django.shortcuts import render, get_object_or_404, redirect
from .models import Detailed_desc
from .forms import PlacesForm





from django.core.exceptions import ObjectDoesNotExist

import random

#  __lte=      is eqivelent to lessthan or euivelent
#    table.all().filter().exclude().filer()   for two filters and one excluding condition
# Create your views here.

def index(request):
    dests = Destination.objects.all()
    dest1 = []
    j=0
    try:
        temp = Detailed_desc.objects.get(dest_id=j)
        dest1.append(temp)
    except ObjectDoesNotExist:
        print("don't")
    return render(request, 'index.html', {'dests': dests, 'dest1': dest1})

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, last_name=last_name,
                                                first_name=first_name)
                user.save()
                print('user Created')
                return redirect('login')
        else:
            messages.info(request, 'Password is not matching ')
            return redirect('register')
        return redirect('index')
    else:
        return render(request, 'register.html')

def adminbooking(request):
    person = pessanger_detail.objects.all()
    return render(request, 'admin_booking.html',{"person":person})


def adminviewuser(request):
    users = User.objects.all()
    return render(request, 'admin_viewusers.html', {'users': users})


def admin_destination(request):
    travello_destination = Destination.objects.all()
    travello_detailed_desc = Detailed_desc.objects.all()

    context = {
        'travello_destination': travello_destination,
        'travello_detailed_desc': travello_detailed_desc,
    }

    return render(request, 'admin_destination.html', context)



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == '7894561230' and password == 'admin':
            return render(request, 'admin_home.html')
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Sucessfully Logged in')
            email = request.user.email
            print(email)
            content = 'Hello ' + request.user.first_name + ' ' + request.user.last_name + '\n' + 'You are logged in in our site.keep connected and keep travelling.'
            dests = Destination.objects.all()
            return render(request, 'index.html',{'dests':dests})
        else:
            messages.info(request, 'Invalid credential')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect("/")



@login_required(login_url='login')
def destination_list(request,city_name):
    dests = Detailed_desc.objects.all().filter(country=city_name)
    return render(request,'travel_destination.html',{'dests': dests})


def destination_details(request,city_name):
    dest = Detailed_desc.objects.get(dest_name=city_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request,'destination_details.html',{'dest':dest})

def search(request):
    try:
        request.session['place'] = request.POST.get('place')

        place1 = request.session.get('place')


       
        
        dest = Detailed_desc.objects.get(dest_name=place1)
        print(place1)
        return render(request, 'destination_details.html', {'dest': dest})
    except:
        messages.info(request, 'Place not found')
        return redirect('index')

class KeyValueForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()
def pessanger_detail_def(request, city_name):
    print ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAss")
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            date1 = datetime.now().date()
            if temp_date < date1:
                return redirect('index')
            obj = pessanger_detail.objects.get(Trip_id=17)
            pipo_id = obj.Trip_same_id
            #pipo_id =4
            request.session['Trip_same_id'] = pipo_id
            price = request.session['price']
            city = request.session['city']
            print(request.POST['trip_date'])
            #temp_date = parse_date(request.POST['trip_date'])
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            usernameget = request.user.get_username()
            print(temp_date)
            request.session['n']=formset.total_form_count()
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]

                t = pessanger_detail(Trip_same_id=pipo_id,first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                     age=form.cleaned_data['age'],
                                     Trip_date=temp_date,payment=price,username=usernameget,city=city)
                t.save()
                # print (formset.forms[i].form-[i]-value)

            obj.Trip_same_id = (pipo_id + 1)
            obj.save()
            no_of_person = formset.total_form_count()
            price1 = no_of_person * price
            GST = price1 * 0.18
            GST = float("{:.2f}".format(GST))
            final_total = GST + price1
            request.session['pay_amount'] = final_total
            return render(request,'payment.html', {'no_of_person': no_of_person,
                                                   'price1': price1, 'GST': GST, 'final_total': final_total,'city': city })
    else:
        formset = KeyValueFormSet()

        return render(request, 'sample.html', {'formset': formset, 'city_name': city_name, })


def upcoming_trips(request):
    username = request.user.get_username()
    date1=datetime.now().date()
    person = pessanger_detail.objects.all().filter(username=username).filter(pay_done=1)
    person = person.filter(Trip_date__gte=date1)
    print(date1)
    return render(request,'upcoming trip1.html',{'person':person})

@login_required(login_url='login')
def card_payment(request):
    try:
        # print("if ma gayu")
        # rno = random.randint(100000, 999999)
        # request.session['OTP'] = rno
        request.session['OTP'] = 12345

        # amt = request.session['pay_amount']
        # username = request.user.get_username()
        # print(username)
        # user = User.objects.get(username=username)
        # mail_id = user.email
        # print([mail_id])
        # msg = 'Your OTP For Payment of ₹' + str(amt) + ' is ' + str(rno)
        # # print(msg)
        # # print([mail_id])
        # # print(amt)
        # send_mail('OTP for Debit card Payment',
        #             msg,
        #             'travellotours89@gmail.com',
        #             [mail_id],
        #             fail_silently=False)
        return render(request, 'OTP.html')
    
    except:
        return render(request, 'wrongdata.html')

# recomendation
@login_required(login_url='login')
def new_page_view(request):
     if request.method == 'POST':
         price=int(request.POST['price'])
         day= int(request.POST['days'])
         food = int(request.POST['food'])
         stay = int(request.POST['stay'])
         climate = int(request.POST['climate'])
         fsize = int(request.POST['family-size'])
         transport = int(request.POST['transport'])
         activity = int(request.POST['activity'])
        #  dest = request.POST['place']
        #  obj = Suggestion(price=price,days=day,food=food,stay=stay,climate=climate,size=fsize,transport=transport,activity=activity,destination=dest)
        #  obj.save()
        # sql table conversion to pandas and KNN
         queryset = Suggestion.objects.all()
         data = list(queryset.values())
         df = pd.DataFrame(data)

         df1 = df[['price','days','food','stay','climate','size','transport','activity']].copy()
         target=df[['destination']].copy()
         df1['price'] = df1['price'].astype(int)
         df1['days'] = df1['days'].astype(int)
         df1['food'] = df1['food'].astype(int)
         df1['stay'] = df1['stay'].astype(int)
         df1['climate'] = df1['climate'].astype(int)
         df1['size'] = df1['size'].astype(int)
         df1['transport'] = df1['transport'].astype(int)
         df1['activity'] = df1['activity'].astype(int)

         dest_dict = {0: "Rome", 1: "Venice", 2: "Florence", 3: "Pisa", 4: "The Dubai Mall", 5: "Burj Khalifa", 6: "Dubai Marina", 7: "Kite Beach by Meraas", 8: "New York", 9: "Las Vegas", 10: "Isaland", 11: "Lord Howe Island", 12: "Global Village", 13: "Ski Dubai", 14: "Bali", 15: "Paris", 16: "Versailles", 17: "Yogyakarta", 18: "London", 19: "Berlin", 20: "Taj Mahal", 21: "Jaipur City Palace", 22: "Amalfi Coast", 23: "Nice", 24: "Lyon", 25: "Bordeaux", 26: "Lombok", 27: "Jakarta", 28: "Raja Ampat Islands", 29: "Oxford", 30: "Bath", 31: "Cambridge", 32: "Liverpool", 33: "York", 34: "Brighton", 35: "Manchester", 36: "Munich", 37: "Hamburg", 38: "Cologne", 39: "Heidelberg", 40: "Udaipur", 41: "Varanasi", 42: "Kerala Backwaters", 43: "Strasbourg", 44: "Annecy", 45: "Colmar", 46: "Avignon", 47: "Lille"}


        #  data_val = data.values
         target_val = target['destination'].tolist()
        #  knn = KNeighborsClassifier(n_neighbors=3)
        #  knn.fit(df1,target_val)
         clf = RandomForestClassifier(n_estimators=100)  # You can adjust the number of trees (n_estimators) and other hyperparameters
         clf.fit(df1,target_val)
         result = clf.predict([[price,day,food,stay,climate,fsize,transport,activity]])
        #  print(price,day,food,stay,climate,fsize,transport,activity)
        #  print(dest_dict[result[0]])
         return redirect(f"/destination_list/destination_details/{dest_dict[result[0]]}")
     else:
         return render(request,'new_page.html')
        


@login_required(login_url='login')
def net_payment(request):
    username = request.POST['cardNumber']
    Password1 = request.POST['pass']
    Bank_name = request.POST['banks']
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Net Banking'
    try:
        r = NetBanking.objects.get(Username=username, Password=Password1,Bank=Bank_name)
        balance = r.Balance
        request.session['total_balance'] = balance
        if int(balance) >= int(request.session['pay_amount']):
            total_balance = int(request.session['total_balance'])
            rem_balance = int(total_balance - int(request.session["pay_amount"]))
            r.Balance = rem_balance
            r.save(update_fields=['Balance'])
            r.save()
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
            t.save()
            return render(request, 'confirmetion_page.html')
        else:
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
            t.save()
            return render(request, 'wrongdata.html')
    except NetBanking.DoesNotExist:
        return render(request, 'wrongdata.html', {'error_message': 'Invalid username, password, or bank.'})
    except Exception as e:
        return render(request, 'wrongdata.html', {'error_message': str(e)})


@login_required(login_url='login')
def otp_verification(request):
    otp1 = int(request.POST['otp'])
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Debit card'
    if otp1 == int(request.session['OTP']):
        del request.session["OTP"]
        # total_balance = int(request.session['total_balance'])
        # rem_balance = int(total_balance-int(request.session["pay_amount"]))
        # c = Cards.objects.get(Card_number=request.session['dcard'])
        # c.Balance = rem_balance
        # c.save(update_fields=['Balance'])
        # c.save()
        # t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
        # t.save()
        z = pessanger_detail.objects.all().filter(Trip_same_id=Trip_same_id1)
        for obj in z:
            obj.pay_done = 1
            obj.save(update_fields=['pay_done'])
            obj.save()
            print(obj.pay_done)
        return render(request, 'confirmetion_page.html')
    else:
        # t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
        # t.save()
        return render(request, 'wrong_OTP.html')

@login_required(login_url='login')
def data_fetch(request):
    username = request.user.get_username()
    person = pessanger_detail.objects.all().filter(username=username)



def admin_home(request):
    return render(request, 'admin_home.html')



def delete_booking(request, trip_id):
    if request.method == 'POST':
        booking = get_object_or_404(pessanger_detail, Trip_id=trip_id)
        booking.delete()
        return redirect('adminbooking')  
    else:
        pass


def delete_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        user.delete()
    return redirect('admin_viewusers')



def delete_country(request, country_id):
    if request.method == 'POST':
        country = Destination.objects.get(id=country_id)
        country.delete()  
        return redirect('admin_destination')
    


def delete_detailed_desc(request, detailed_desc_id):
    if request.method == 'POST':
        detailed_desc = Detailed_desc.objects.get(dest_id=detailed_desc_id)
        detailed_desc.delete()
    return redirect('admin_destination')



def edit_country(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            # Redirect to some URL after successful edit
            return redirect('admin_destination')
    else:
        form = CountryForm(instance=destination)
    
    return render(request, 'edit_country.html', {'form': form})



def edit_places(request, detailed_desc_id):
    detailed_desc = get_object_or_404(Detailed_desc, dest_id=detailed_desc_id)
    if request.method == 'POST':
        form = PlacesForm(request.POST, request.FILES, instance=detailed_desc)
        if form.is_valid():
            form.save()
            return redirect('admin_destination')  
    else:
        form = PlacesForm(instance=detailed_desc)
    
    return render(request, 'edit_places.html', {'form': form})