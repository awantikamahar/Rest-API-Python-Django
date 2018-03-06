from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.conf import settings
from collections import namedtuple


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    user_role = RoleSerializer()

    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'email', 'user_role')


###############Employee Document################
class EmployeeDocumentSerializer(serializers.ModelSerializer):
    document_name = serializers.CharField(required=False, allow_blank=True)
    document_description = serializers.CharField(required=False, allow_blank=True)
    file_type = serializers.CharField(required=False, allow_blank=True)
    verified = serializers.BooleanField(required=False)

    class Meta:
        model = EmployeeDocument
        fields = '__all__'


################Employee Document Ends###############

class AppliedLeaveListSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)

    class Meta:
        model = AppliedLeave
        fields = ['id', 'user', 'type_of_leave', 'leave_from', 'to_leave', 'number_of_days', 'reason', 'appliedOn', 'actionOn']


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'


class AppliedLeaveSerializer(serializers.ModelSerializer):
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)
    class Meta:
        model = AppliedLeave
        fields = ('id', 'user', 'type_of_leave', 'leave_from', 'to_leave', 'number_of_days', 'reason', 'appliedOn')


class LeavesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Leaves
        fields = [
                    'id', 
                    'balance_sick_leave', 
                    'total_sick_leave',
                    'balance_casual_leave',
                    'total_casual_leave',
                    'balance_earned_leave',
                    'total_earned_leave',
                    'balance_compoff_leave',
                    'total_compoff_leave',
                    'user'
                    ]


class BalanceLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ('id', 'balance_sick_leave', 'total_sick_leave', 'balance_casual_leave', 'total_casual_leave', 'balance_earned_leave', 'total_earned_leave', 'balance_compoff_leave', 'total_compoff_leave')



class ManagerLeaveViewSerializer(serializers.ModelSerializer):
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)
    class Meta:
        model = AppliedLeave
        # fields = ('id', 'type_of_leave', 'leave_from', 'to_leave', 'number_of_days', 'appliedOn')
        fields = [
            'id',
            'type_of_leave',
            'leave_from',
            'to_leave',
            'number_of_days',
            'status',
            'appliedOn',
            'approvedBy',
            'actionOn',
            'reason',
            'declined'
            ]


class AppliedLeaveHistory(serializers.ModelSerializer):
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)
    class Meta:
        model = AppliedLeave
        fields = '__all__'

class AppliedLeaveUpdate(serializers.ModelSerializer):
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)
    class Meta:
        model = AppliedLeave
        fields = ('id', 'user', 'type_of_leave', 'leave_from', 'to_leave', 'number_of_days', 'reason', 'appliedOn', 'actionOn', 'declined')

        
class EmployeesLeaveForManager(serializers.ModelSerializer):
    user_role = RoleSerializer()
    users_leave = ManagerLeaveViewSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'user_role', 'users_leave')

#####---Leave Ends------############



##########--------------Add New Employee to the organization------------#########
class AddNewEmployeeSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    pincode = serializers.IntegerField(required=False)
    father_name = serializers.CharField(required=False, allow_blank=True)
    mother_name = serializers.CharField(required=False, allow_blank=True)
    pan_card = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Employees
        fields = [
            'user',
            'phone_no',
            'email',
            'address',
            'city',
            'pincode',
            'father_name',
            'mother_name',
            'pan_card'
        ]
##########-------------------------HR Payrole-----------##############

class HrUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'user_role']


##########----------------------Bank Details----------###############

class BankDetailsSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(required=False, allow_blank=True)
    bmicr_code = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = BankDetails
        fields = '__all__'


#########----------------------Salary Serializer----------############
class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'



class HrUserDetailSerializer(serializers.ModelSerializer):
    employee_salary = SalarySerializer(many=False)
    employee_bank = BankDetailsSerializer(many=False)
    user_role = RoleSerializer(many=False)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'employee_salary', 'employee_bank', 'user_role']

#########------------Approve Employee serializer--------############
class ApproveEmployeeDetails(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'


class ApproveEmployeesSerializer(serializers.ModelSerializer):
    user_role = RoleSerializer(many=False)
    employee_other_details = ApproveEmployeeDetails()
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'user_role',
            'employee_other_details'
        ]

######---------------Requested Salaries-----------##############
class SalaryRequestedUserSerializer(serializers.ModelSerializer):
    employee_bank = BankDetailsSerializer(many=False)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'employee_bank']

class SalaryRequestedSerializer(serializers.ModelSerializer):
    user = SalaryRequestedUserSerializer(many=False)
    class Meta:
        model=SalaryRequest
        fields = '__all__'

class SalaryRequestPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryRequest
        fields = '__all__'