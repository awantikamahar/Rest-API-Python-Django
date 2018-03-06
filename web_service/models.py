import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import uuid
import datetime



@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class RoleTypes(models.Model):
    role_type = models.CharField(max_length=20)


class Role(models.Model):
    user = models.OneToOneField(User, related_name='user_role', on_delete=models.CASCADE)
    role_type = models.CharField(max_length=20)
    department = models.CharField(max_length=20)




class Employees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_other_details')
    phone_no = models.CharField(max_length=13, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.IntegerField(null=True)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    mother_name = models.CharField(max_length=50, null=True, blank=True)
    pan_card = models.CharField(max_length=100,  null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    approved_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name




class EmployeeDocument(models.Model):
    user = models.ForeignKey(User, related_name='user_document', on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100, null=True, blank=True)
    ducument_file = models.FileField(null=True, blank=True)
    document_description = models.CharField(max_length=200, null=True, blank=True)
    file_type = models.CharField(max_length=20, null=True, blank=True)
    verified = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user+' '+self.document_name


class Department(models.Model):
    name = models.CharField(max_length=20)



class Holiday(models.Model):
    date = models.DateField(null=False)
    reason = models.CharField(max_length=500, null=True,blank=True)

    def __str__(self):
        return self.reason


class Leaves(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance_sick_leave = models.FloatField()
    total_sick_leave = models.FloatField()
    balance_casual_leave = models.FloatField()
    total_casual_leave = models.FloatField()
    balance_earned_leave = models.FloatField()
    total_earned_leave = models.FloatField()
    balance_compoff_leave = models.FloatField()
    total_compoff_leave = models.FloatField()
    total_lop = models.FloatField(default=0)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name

class EmployeeLop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appliedOn = models.DateField(auto_now_add=True)
    count = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name


class AppliedLeave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type_of_leave = models.CharField(max_length=100)
    leave_from = models.DateField(null=True,blank=True)
    to_leave = models.DateField(null=True,blank=True)
    number_of_days = models.FloatField(max_length=5)
    reason = models.CharField(max_length=200, null=True,blank=True)
    status = models.BooleanField(default=False)
    appliedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_leave')
    approvedBy = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='approved_by',blank=True)
    appliedOn = models.DateField(auto_now_add=True, null=False)
    actionOn = models.DateTimeField(null=True,blank=True)
    declined = models.BooleanField(default=False)
    # end_date-start_date

    def save(self, *args, **kwarg):
        start_date = datetime.datetime.strptime(str(self.leave_from), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(str(self.to_leave), "%Y-%m-%d")
        diff = abs((end_date-start_date).days)
        print(diff)
        self.number_of_days = diff
        super(AppliedLeave, self).save(*args, **kwarg)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name




#####------------------HR Payrole------------------#####

class BankDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_bank')
    bank_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=50)
    account_type = models.CharField(max_length=20)
    bank_address = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=13, null=True, blank=True)
    bmicr_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.first_name+' '+self.bank_name


class Salary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_salary')
    basic = models.FloatField()
    hra = models.FloatField()
    conveyance_allowance = models.FloatField(null=True)
    misc_allowance = models.FloatField(null=True)
    proffesional_tax = models.FloatField(null=True)
    net_salary = models.FloatField(null=True)
    net_salary_anum = models.FloatField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def calculate_net_salary(self):
        calculate_salary = self.basic+self.hra+self.conveyance_allowance+self.misc_allowance
        tax = (calculate_salary/100)*self.proffesional_tax
        net_salary = calculate_salary - tax
        return net_salary

    @property
    def calculate_net_salary_anum(self):
        net_salary_anum = self.net_salary * 12
        return net_salary_anum

    def save(self, *args, **kwarg):
        self.net_salary = self.calculate_net_salary
        self.net_salary_anum = self.calculate_net_salary_anum
        super(Salary, self).save(*args, **kwarg)

class SalaryRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salaries')
    basic = models.FloatField(null=True)
    hra = models.FloatField(null=True)
    conveyance_allowance = models.FloatField(null=True)
    deduction = models.FloatField(null=True)
    misc_allowance = models.FloatField(null=True)
    proffesional_tax = models.FloatField(null=True)
    net_salary = models.FloatField(null=True)
    net_salary_paybale = models.FloatField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    credited = models.BooleanField(default=False)
    credited_on = models.DateTimeField(null=True)

    # @property
    # def calculate_net_salary(self):
    #     calculate_salary = self.basic+self.hra+self.conveyance_allowance+self.misc_allowance
    #     tax = (basic_salary/100)*self.proffesional_tax
    #     net_salary = calculate_salary - tax
    #     return net_salary

    # @property
    # def calculate_deduction(self):
    #     deduction = self.net_salary - self.deduction
    #     return deduction

    def save(self, *args, **kwarg):
        # self.net_salary = self.calculate_net_salary
        # self.deduction = self.calculate_deduction
        self.net_salary_paybale = self.net_salary-self.deduction
        super(SalaryRequest, self).save(*args, **kwarg)

