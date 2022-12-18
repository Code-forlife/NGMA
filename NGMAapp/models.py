from django.db import models

# Create your models here.
class VisiterForm(models.Model):
    FName=models.CharField(max_length=122)
    LName=models.CharField(max_length=122)
    Booking_Date=models.DateField()
    Email=models.EmailField(max_length=122)
    Timing=models.TimeField()
    NoC=models.PositiveIntegerField()
    NoA=models.PositiveIntegerField()
    PhoneNo=models.CharField(max_length=107)
    Booking_time=models.TimeField()
    def __str__(self):
        return self.FName+" "+self.LName
    
class VisitorDetails(models.Model):
    FName=models.CharField(max_length=122)
    LName=models.CharField(max_length=122)
    Email=models.EmailField(max_length=122)
    PhoneNo=models.CharField(max_length=107)
    username=models.CharField(max_length=122)
    Age=models.PositiveIntegerField()
    def __str__(self):
        return self.FName+" "+self.LName
    
class ArtistDetails(models.Model):
    FName=models.CharField(max_length=122)
    LName=models.CharField(max_length=122)
    Email=models.EmailField(max_length=122)
    PhoneNo=models.PositiveIntegerField()
    username=models.CharField(max_length=122)
    Age=models.PositiveIntegerField()
    def __str__(self):
        return self.FName+" "+self.LName
    
class ArtistForms(models.Model):
    First_Name=models.CharField(max_length=122)
    Last_Name=models.CharField(max_length=122)
    Age=models.PositiveIntegerField()
    PhoneNo=models.CharField(max_length=107)
    Email=models.EmailField(max_length=122)
    Specialization=models.CharField(max_length=255)
    Achievements=models.FileField(upload_to='ArtistForm/images',default="")
    Art=models.FileField(upload_to='ArtistForm/images',default="")
    def __str__(self):
        return self.First_Name+" "+self.Last_Name
    
from django.utils import timezone
class Transaction(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    First_Name=models.CharField(max_length=122)
    Last_Name=models.CharField(max_length=122)
    PhoneNo=models.CharField(max_length=107)
    Email=models.EmailField(max_length=122)
    Address=models.TextField(null=True)
    Address2=models.TextField(default="Nothing")
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    Country=models.CharField(max_length=255,null=True)
    States=models.CharField(max_length=255,null=True)
    zipcode=models.PositiveBigIntegerField(null=True)
    Payment_NoA=models.PositiveIntegerField(null=True)
    Payment_NoC=models.PositiveIntegerField(null=True)
    Total_Amount=models.PositiveBigIntegerField(null=True)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    #razorpay related
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.First_Name+" "+self.Last_Name
    
class Employees(models.Model):
    Department_choice = (
        (1,'Select'),
        (2, 'Receptionist'),
        (3, 'Security'),
        (4, 'Management'),
        (5,'Tech')
    )
    First_Name=models.CharField(max_length=122)
    Last_name=models.CharField(max_length=122)
    Employee_ID=models.IntegerField(primary_key=True)
    Designation=models.CharField(max_length=122)
    PhoneNo=models.CharField(max_length=107)
    Email=models.EmailField(max_length=122)
    Age=models.PositiveIntegerField()
    DOB=models.DateField()
    Blood_Group=models.CharField(max_length=107)
    Address=models.TextField()
    DOJ=models.DateField()
    Department=models.IntegerField(choices=Department_choice,default=1)
    username=models.CharField(max_length=122)
    photo=models.ImageField(null=True)
    def __str__(self):
        return self.First_Name+" "+self.Last_name
    
class ReviewSection(models.Model):
    First_Name=models.CharField(max_length=122)
    Last_Name=models.CharField(max_length=122)
    Email=models.EmailField(max_length=122)
    Username=models.CharField(max_length=122)
    STAR=models.IntegerField()
    Feedback=models.TextField()
    def __str__(self):
        return self.First_Name+" "+self.Last_Name
    
    