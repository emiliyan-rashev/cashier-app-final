from django.db import models
import datetime

class PaymentsAdmin(models.Model):
    individual_monthly_tax = models.IntegerField(default=0)
    salaries = models.IntegerField(default=0)

class TaxesPerMonth(models.Model):
    January = models.IntegerField(default=0)
    February = models.IntegerField(default=0)
    March = models.IntegerField(default=0)
    April = models.IntegerField(default=0)
    May = models.IntegerField(default=0)
    June = models.IntegerField(default=0)
    July = models.IntegerField(default=0)
    August = models.IntegerField(default=0)
    September = models.IntegerField(default=0)
    October = models.IntegerField(default=0)
    November = models.IntegerField(default=0)
    December = models.IntegerField(default=0)

class SalariesPerMonth(models.Model):
    January = models.IntegerField(default=0)
    February = models.IntegerField(default=0)
    March = models.IntegerField(default=0)
    April = models.IntegerField(default=0)
    May = models.IntegerField(default=0)
    June = models.IntegerField(default=0)
    July = models.IntegerField(default=0)
    August = models.IntegerField(default=0)
    September = models.IntegerField(default=0)
    October = models.IntegerField(default=0)
    November = models.IntegerField(default=0)
    December = models.IntegerField(default=0)

class IndividualPayment(models.Model):
    January = models.BooleanField(default=False)
    February = models.BooleanField(default=False)
    March = models.BooleanField(default=False)
    April = models.BooleanField(default=False)
    May = models.BooleanField(default=False)
    June = models.BooleanField(default=False)
    July = models.BooleanField(default=False)
    August = models.BooleanField(default=False)
    September = models.BooleanField(default=False)
    October = models.BooleanField(default=False)
    November = models.BooleanField(default=False)
    December = models.BooleanField(default=False)

#Трябва да имa история на таксите за всеки месец
#Също трябва да се направи някакъв сигнал може би, когато се промени таксата да я ъпдейтва за определени месеци. Може и да се добави едно радио, което админът да избира, когато ъпдейтва таксата