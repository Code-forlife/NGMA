from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.shortcuts import redirect, render
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
# pdf generator
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
# from .tokens import generate_token
from django.contrib.auth.decorators import login_required
# Imported Models
from NGMAapp.models import ArtistForms, Employees, VisiterForm, VisitorDetails, ArtistDetails, Transaction, ReviewSection
from NGMA import settings

# Create your views here.

# no fancy thing going 
def home(request):
    return render(request,'Home.html')
def Booking(request):
    return render(request,'Booking.html')
def Contact(request):
    return render(request,'ContactUs.html')
def About(request):
    return render(request,'AboutUs.html')
def Artist(request):
    return render(request,'ArtistPage.html')
import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))
# Visitor form #razorpay integration
def VisitorForm(request):
    if request.user.is_anonymous or not(VisitorDetails.objects.filter(username=request.user.username).exists()):
        return redirect("/LoginUser")
    username=request.user.username
    FName=request.user.first_name
    LName=request.user.last_name
    Email=request.user.email
    account=VisitorDetails.objects.filter(username=username)[0]

    if request.method == "POST":
        NoA=request.POST['NoA']
        Booking_Date=request.POST['Booking_Date']
        NoC=request.POST['NoC']
        Timing=request.POST['Timing']
        visitor=VisiterForm(FName=FName, LName=LName,Booking_Date=Booking_Date,Email=Email,PhoneNo=account.PhoneNo,Timing=Timing,NoC=NoC, NoA= NoA,Booking_time=timezone.now())
        visitor.save()
        return redirect('/Checkout')
    return render(request,'VisitorForm.html',{'username':username,'fname':FName,'lname':LName,'email':Email,'phoneno':account.PhoneNo})

def ArtistForm(request):
    if request.user.is_anonymous or  not(ArtistDetails.objects.filter(username=request.user.username).exists()):
        return redirect("/LoginUser")
    username=request.user.username
    FName=request.user.first_name
    LName=request.user.last_name
    Email=request.user.email
    account=ArtistDetails.objects.filter(username=username)[0]
    if request.method == "POST":
        FName=request.POST.get('FName')
        LName=request.POST.get('LName')
        PhoneNo=request.POST.get('PhoneNo')
        Age=request.POST.get('Age')
        Email=request.POST.get('Email')
        Specialization=request.POST.get('Specialization')
        Achievements=request.POST.get('Achievements')
        Art=request.POST.get('Art')
        Artist= ArtistForms(First_Name=FName, Last_Name=LName,Email=Email, PhoneNo=PhoneNo,Age=Age,Specialization=Specialization,Achievements=Achievements,Art=Art)
        Artist.save()
        messages.success(request,"Your form has been submitted")
        # render(request,'Error.html')
        
    return render(request,'ArtistForm.html',{'username':username,'fname':FName,'lname':LName,'email':Email,'phoneno':account.PhoneNo,'age':account.Age})

@login_required
def Checkout(request):
    username=request.user.username
    FName=request.user.first_name
    LName=request.user.last_name
    Email=request.user.email
    accounts=VisiterForm.objects.filter(Email=Email,FName=FName).last()
    
    price_NoA=75
    price_NoC=50
    
    Total_Price_NoA=int(price_NoA)* int(accounts.NoA)
    Total_Price_NoC=int(price_NoC)* int(accounts.NoC)
    Total_Amount=int(Total_Price_NoC)+int(Total_Price_NoA)
    if request.method=="POST":
        Address=request.POST['Address']
        Address2=request.POST['Address2']
        Country=request.POST['Country']
        States=request.POST['State']
        zipcode=request.POST['zip']
        transaction=Transaction(First_Name=FName,Last_Name=LName,Email=Email,PhoneNo=accounts.PhoneNo,Address=Address,Address2=Address2,Country=Country,States=States,zipcode=zipcode,Payment_NoA=Total_Price_NoA,Payment_NoC=Total_Price_NoC,Total_Amount=Total_Amount)
        transaction.save()
        order_currency = 'INR'
        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
        razorpay_order = razorpay_client.order.create(dict(amount= int(Total_Amount)*100, currency=order_currency, receipt=transaction.order_id, payment_capture='0'))
        transaction.razorpay_order_id = razorpay_order['id']
        transaction.save()
        return render(request,'summary.html',{'username':username,'fname':FName,'lname':LName,'email':Email,'phoneno':accounts.PhoneNo,'pNoA':Total_Price_NoA,'pNoC':Total_Price_NoC,'Total':Total_Amount,'order_id': razorpay_order['id'], 'orderId':transaction.order_id, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})
    return render(request,'Checkout.html',{'username':username,'fname':FName,'lname':LName,'email':Email,'phoneno':accounts.PhoneNo,'pNoA':Total_Price_NoA,'pNoC':Total_Price_NoC,'Total':Total_Amount})

def LoginUser(request):
    if request.method=='POST':
        username=request.POST['Username']
        password=request.POST['Password']
        type=request.POST['Type-of-account']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            if type=="Employee" and Employees.objects.filter(username=username).exists():
                return redirect("Employee/")
            elif type=="Visitor" and VisitorDetails.objects.filter(username=username).exists():
                return redirect("VisitorForm/",{'username':username})
            elif type=="Artist" and ArtistDetails.objects.filter(username=username).exists():
                return redirect("ArtistForm/")
            else:
                messages.error(request,"Wrong Username or Password")
        else:
            messages.error(request,"Wrong Username or Password")
            return render(request,'Login.html')
    return render(request,'Login.html')

def LogoutUser(request):
    logout(request)
    return redirect("Home/")

def Register(request):
    if request.method=='POST':
        # username=request.POST.get('Username')
        username=request.POST['Username']
        password=request.POST['Password']
        Fname=request.POST['Fname']
        Lname=request.POST['Lname']
        Email=request.POST['Email']
        PhoneNo =request.POST['PhoneNo']
        Age=request.POST['Age']
        Type=request.POST['Type-of-account']
        if User.objects.filter(username=username) or ArtistDetails.objects.filter(username=username).exists() or VisitorDetails.objects.filter(username=username).exists():
            messages.error(request,"Username already exits! Please try some other username.")
        if  User.objects.filter(email=Email) or ArtistDetails.objects.filter(Email=Email).exists() or VisitorDetails.objects.filter(Email=Email).exists():
            messages.error(request,"Email ID already exits! Please try some other Email ID.") 
        myuser =User.objects.create_user(username,Email,password)
        myuser.first_name=Fname
        myuser.last_name=Lname
        # myuser.is_active = True
        myuser.save()
        if Type=='Visitor':
            visitordetails=VisitorDetails(FName=Fname, LName=Lname,Email=Email, PhoneNo=PhoneNo,Age=Age,username=username)
            visitordetails.save()
        elif Type=='Artist':
            artistdetails=ArtistDetails(FName=Fname, LName=Lname,Email=Email, PhoneNo=PhoneNo,Age=Age,username=username)
            artistdetails.save()

        # messages.success(request,"Your Account has been successfully created.")
        #Welcome Email
        subject ="Welcome to the largest Community of art"
        message="Hello there!! "+ Fname+"\nWelcome to some place where you can share your art ,learn about different forms of art and teach your creative students about your art\n"+"We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nPranay Singhvi"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ NGMA Login!!"
        message2 = render_to_string('email_confirmation.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': account_activation_token.make_token(myuser)
        })
        emails = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )       
        emails.send(fail_silently = True)
        return redirect('LoginUser/')
    return render(request,'Register.html')

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and account_activation_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('VisitorForm/')
    else: 
        return render(request,'activation_failed.html')
    

def Employee(request):
    if request.user.is_anonymous and request.user.is_staff or not (Employees.objects.filter(username=request.user.username).exists()):
        return redirect("/LoginUser")
    username=request.user.username
    FName=request.user.first_name
    LName=request.user.last_name
    Email=request.user.email
    empl=Employees.objects.filter(username=username,First_Name=FName,Email=Email)[0]
    if empl.Department==5:
        return render(request,'Employee.html',{'fname':FName,'lname':LName,'email':Email,'empl':empl,'dep':"Tech"})
    elif empl.Department==4:
        return render(request,'Employee.html',{'fname':FName,'lname':LName,'email':Email,'empl':empl,'dep':"Management"})
    elif empl.Department==3:
        return render(request,'Employee.html',{'fname':FName,'lname':LName,'email':Email,'empl':empl,'dep':"Security"})
    elif empl.Department==2:
        return render(request,'Employee.html',{'fname':FName,'lname':LName,'email':Email,'empl':empl,'dep':"Receptionist"})
    
    
    return render(request,'Employee.html',{'fname':FName,'lname':LName,'email':Email,'empl':empl})

def Review(request):
    if request.user.is_anonymous and not(VisitorDetails.objects.filter(username=request.user.username).exists()):
        return redirect("/LoginUser")
    if request.method=="POST":
        username=request.user.username
        FName=request.user.first_name
        LName=request.user.last_name
        Email=request.user.email
        star=request.POST['rate']
        feedback=request.POST['Feedback']
        section=ReviewSection(First_Name=FName,Last_Name=LName,Username=username,Email=Email,STAR=star,Feedback=feedback)
        section.save()
        messages.success(request,"Your form has been submitted")
    return render(request,'Review.html')


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = Transaction.objects.filter(razorpay_order_id=order_id).last()
            except:
                return render(request,'paymentfailed.html')
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result!=None:
                amount = int(order_db.Total_Amount) * 100   #we have to pass in paisa
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    order_db.payment_status = 1
                    order_db.save()
                    details=VisiterForm.objects.filter(FName=order_db.First_Name,LName=order_db.Last_Name).last()
                    return render(request, 'Confir.html',{'order':order_db,'details':details})
                except:
                    order_db.payment_status = 2
                    order_db.save()
                    return HttpResponse("Failed")
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request,'paymentfailed.html')
        except:
            return render(request,'paymentfailed.html')

#for pdf generator

def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
class GenerateInvoice(View):
    def get(self, request, pk, *args, **kwargs):
        # try:
        order_db = Transaction.objects.get(id = pk, First_Name = request.user.first_name, payment_status = 1)
        Visitor = VisiterForm.objects.filter(Email=request.user.email , FName = request.user.first_name)[0] #you can filter using order_id as well
        # except:
        #     return HttpResponse("505 Not Found")
        data = {
            'order_id': order_db.order_id,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': request.user.email,
            'date': str(order_db.datetime_of_payment),
            'fname': request.user.first_name,
            'lname': request.user.last_name,
            'order': order_db,
            'visit': Visitor,
            'amount': order_db.Total_Amount,
        }
        pdf = render_to_pdf('invoice.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")