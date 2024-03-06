from django.db import models

# Create your models here.
class Student(models.Model):
    reg_no = models.CharField(primary_key=True,max_length=50)
    name = models.CharField(max_length=250)
    pin = models.IntegerField(null=True)
    fee_balance = models.FloatField()
    phone = models.CharField(max_length=20,unique=True,null=True)
    email = models.EmailField(null=True)
    admission_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    mpesa_code = models.CharField(max_length=50,null=True)
    amount = models.FloatField()
    phone = models.CharField(max_length=20,null=True)
    date = models.DateField(auto_now=True)
    student_reg = models.CharField(max_length=50,null=True,blank=True)
    
    
    def __str__(self):
        return self.phone
    
class Fees(models.Model):
    pass
    