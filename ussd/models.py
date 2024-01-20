from django.db import models

# Create your models here.
class Student(models.Model):
    reg_no = models.CharField(primary_key=True,max_length=50)
    name = models.CharField(max_length=250)
    pin = models.IntegerField(null=True)
    fee_balance = models.FloatField()
    phone = models.CharField(max_length=20,unique=True,null=True)
    
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    id = models.CharField(max_length=30,primary_key=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    amount = models.FloatField()
    
    def __str__(self):
        return self.id
    
class Fees(models.Model):
    pass
    