from django.shortcuts import render
from .models import *
from .serializers import *

from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from annoying.functions import get_object_or_None
from datetime import date

from collections import namedtuple
import time
from datetime import datetime
from time import gmtime, strftime
from django.core.mail import send_mail

# Create your views here.

@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user:
        serializer = UserSerializer(user)
        current_time = timezone.now()
        token = Token.objects.get(user=user)
        return JsonResponse({"user": serializer.data,
                             "token": token.key,
                             "login_time": strftime("%H:%M:%S", time.localtime())
                             }, status=200)
    else:
        return JsonResponse({"message": "invalid credentials"}, status=401)


@api_view(['GET'])
def logout(request):
    user= request.user
    if user:
        return JsonResponse({'message': 'User logged out successfully'})
    else:
        return JsonResponse({'message':'Unauthorized User'})


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user is None:
    	password = request.data['password']
    	user_save = User(
    		username = request.data['username']
    		)
    	user_save.set_password(password)
    	user_save.save()
    	user_role = Role(
    		user = user_save,
    		role_type = request.data['role'],
			department = request.data['department']
    		)
    	user_role.save()
    	return JsonResponse({'message': 'User registered successfully'}, status=201)
    return JsonResponse({'message': 'Username already Exists'})


########------------Forgot Password------------############
@api_view(['POST'])
@permission_classes((AllowAny,))
def forgot_password(request):
    user = User.objects.filter(username=request.data['username']).first()
    print(user)
    if user:
        send_mail('subject', 'body of the message', 'mayur.patil1211@gmail.com', ['mayurbppatil@gmail.com'])
        return JsonResponse({'message':'User Exists'}, status=200)
    return JsonResponse({'message':'User not Exists'}, status=400)


########----Add new employee to the Organization-----########
class AddEmployeeView(APIView):
    def post(self, request):
        if request.data:
            email = request.data.get('email', None)
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            role = request.data.get('designation', None)
            department = request.data.get('department', None)
            phone_number = request.data.get('phone_no', None)
            if email:
                user = User.objects.filter(Q(username=email) | Q(email=email)).first()
                print(user)
                if user is None:
                    user_save = User(
                        first_name = first_name,
                        last_name = last_name,
                        username = email
                        )
                    user_save.save()
                    user_role = Role(
                        user = user_save,
                        role_type = role,
                        department = department
                        )
                    user_role.save()
                    request.data["user"] = user_save.id
                    print(request.data)
                    if user_save:
                        try:
                            serializer = AddNewEmployeeSerializer(data=request.data)
                            print('serializer', serializer)
                            if serializer.is_valid():
                                serializer.save()
                                return JsonResponse({'message':'User Added Successfully'}, status=200)
                        except(Exception)as e:
                            print('Exception',e)
                            user_save.delete()
                            user_role.delete()
                            pass
                        return JsonResponse({'message':'Bad String'}, status=400)
                    return JsonResponse({'message':'User Cannot be created, as details are not sufficient'}, status=400)
                return JsonResponse({'message':'User Already Exists'}, status=400)
            return JsonResponse({'message':'Email field is neccessory'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def put(self, request):
        if request.data:
            id = request.data.get('id', None)
            email = request.data.get('email', None)
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            role = request.data.get('designation', None)
            department = request.data.get('department', None)
            phone_number = request.data.get('phone_no', None)
            if email:
                user = User.objects.filter(id=id).first()
                try:
                    if user:
                        user.first_name = first_name
                        user.last_name = last_name
                        user.username = email
                        user.save()
                        user_role = Role.objects.filter(user=user).first()
                        if user_role:
                            user_role.role_type = role
                            user_role.department = department
                            user_role.save()
                        emp_details = Employees.objects.filter(user=user).first()
                        if emp_details:
                            emp_details.phone_no = phone_number
                            emp_details.email = email
                            emp_details.save() 
                        return JsonResponse({'message':'User Updated Successfully'}, status=200) 
                    return JsonResponse({'message':'User Doesn\'t Exists'}, status=400)
                except(Exception)as e:
                    return JsonResponse({'message':'Something Went Wrong, Please try again letter'}, status=400)
            return JsonResponse({'message':'Email field can\'t be blank'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

            

#######-----Approve New Employee----------###########
class ApproveEmployee(APIView):
    def get(self, request):
        employees = Employees.objects.filter(approved=False)
        employee_ids = [i.user.id for i in employees]
        print(employee_ids)
        users = User.objects.filter(id__in=employee_ids)
        print(users)
        serializer = ApproveEmployeesSerializer(users, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        _id = request.data.get('id', None)
        employee = Employees.objects.filter(user=_id).first()
        if employee:
            employee.approved = True
            employee.save()
            user_obj = User.objects.filter(id=employee.user.id).first()
            password = request.data.get('password', None)
            if password:
                user_obj.set_password(password)
            else:
                user_obj.set_password('dscignBiosys')
            user_obj.save()
            return JsonResponse({'message':'User activated, and password has set for the user account'}, status=200)
        return JsonResponse({'message':'Bad Request'}, status=400)


#######-----Add New Employee Ends---------############

"""leavemanagement"""


class HolidayView(APIView):
    """
    Holiday CRUD operation
    """

    def get(self, request, format=None):
        holiday = Holiday.objects.all()
        if holiday:
            serializers = HolidaySerializer(holiday, many=True)
            return Response(serializers.data)
        return JsonResponse({'message': 'Not Found'}, status=405)

    def post(self, request, format=None):
        if request.data:
            serializer = HolidaySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Holiday saved successfully'}, status=200)
            return JsonResponse({'message': 'Bad request'}, status=400)
        return JsonResponse({'message': 'Bad request'}, status=400)


class MainLeaveView(APIView):
    """
    Assign Leave and List Leave
    """

    def get(self, request, format=None):
        # username = request.user.username
        leaves = Leaves.objects.all()
        if leaves:
            serializer = LeavesSerializer(leaves, many=True)
            return Response(serializer.data)
        return JsonResponse({'message': 'Not Found'}, status=404)

    def post(self, request, format=None):
        if request.data:
            user = User.objects.filter(id=request.data['user_id']).first()
            if user:
                try:
                    leaves_instance = Leaves(
                        balance_sick_leave=request.data['total_sick_leave'],
                        total_sick_leave=request.data['total_sick_leave'],
                        balance_casual_leave=request.data['total_casual_leave'],
                        total_casual_leave=request.data['total_casual_leave'],
                        balance_earned_leave=request.data['total_earned_leave'],
                        total_earned_leave=request.data['total_earned_leave'],
                        balance_compoff_leave=request.data['total_compoff_leave'],
                        total_compoff_leave=request.data['total_compoff_leave'],
                        user=user
                    )
                    leaves_instance.save()
                except(KeyError, AttributeError, TypeError)as e:
                    pass
                return JsonResponse({'message': 'Leave assigned successfully'}, status=200)
            return JsonResponse({'message': 'User Not Found'}, status=405)
        return JsonResponse({'message': 'Bad Request'}, status=400)


class AppliedLeaveViewAPI(APIView):
    """
    Applied Leave Class
    """

    def get(self, request, format=None):
        applied_leave = AppliedLeave.objects.filter(status=False, declined=False)
        if applied_leave:
            serializer = AppliedLeaveListSerializer(applied_leave, many=True)
            return Response(serializer.data)
        return JsonResponse({'message': 'Not Found'}, status=404)

    def put(self, request, format=None):
        if request.data:
            print(request.data['id'])
            applied_leave = AppliedLeave.objects.filter(id=request.data['id']).first()
            if applied_leave:
                serializer = AppliedLeaveUpdate(applied_leave, data=request.data)
                print(serializer)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message': 'Updated Successfully'}, status=200)
                return JsonResponse({'message':'Bad String'}, status=405)
            return JsonResponse({'message': 'Leave Not Found'}, status=404)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request, format=None):
        if request.data:
            applied_leave = AppliedLeave.objects.filter(id=request.data['id']).first()
            if applied_leave:
                applied_leave.delete()
                return JsonResponse({'message': 'Leave Deleted Successfully'}, status=200)
            return JsonResponse({'message': 'Leave Not Found'}, status=404)
        return JsonResponse({'message':'Bad Request'}, status=400)


class LeaveUserInfo(APIView):
    def get(self, request, user_id, month, year):
        leave_info = []
        user = User.objects.filter(id=user_id).first()
        if user:
            holidays = Holiday.objects.filter(date__month=month, date__year=year)
            for h in holidays:
                holiday ={
                    'id': h.id,
                    'reason': h.reason,
                    'date': h.date,
                    'type': 'Official'
                }
                leave_info.append(holiday)
            applied_leave = AppliedLeave.objects.filter(user=user, appliedOn__month=month, appliedOn__year=year).all()
            for a in applied_leave:
                applied={
                    'id': a.id,
                    'type_of_leave':a.type_of_leave,
                    'leave_from': a.leave_from,
                    'to_leave': a.to_leave,
                    'number_of_days': a.number_of_days,
                    'status': a.status,
                    'appliedOn':a.appliedOn,
                    'declined':a.declined,
                    'reason': a.reason,
                    'type': 'Applied'
                }
                leave_info.append(applied)
            return JsonResponse({'leave_info': leave_info}, status=200)
        return JsonResponse({'message': 'Un-Recognised User'}, status=400)



class AppliedLeaveUserHistory(APIView):
    def get(self, request, user_id):
        applied_leave = AppliedLeave.objects.filter(appliedBy=user_id)
        serializer = AppliedLeaveHistory(applied_leave, many=True)
        return Response(serializer.data)



@api_view(['GET'])
def leave_info_user(id, *args, **kwargs):
    user = User.objects.filter(id=id).first()
    print(user)
    return JsonResponse({'message': 'Leave assigned successfully'}, status=200)


class EmployeeBalanceLeave(APIView):
	"""
	Check Balance Leave Of Individual Employee
	"""
	def get(self, request, user_id, format=None):
		user = User.objects.filter(id=user_id).first()
		if user:
			leaves = Leaves.objects.filter(user=user).first()
			print(leaves.balance_sick_leave)
			if leaves:
				serializer = BalanceLeaveSerializer(leaves)
				return Response(serializer.data)
			else:
				return JsonResponse({'message':'Leaves Not Found'}, status=405)
		else:
			return JsonResponse({'message': 'User Not Found'}, status=405)


@api_view(['POST'])
def apply_leave(request):
    if request.data:
        user = User.objects.filter(id=request.data['user']).first()
        try:
            reason = request.data['reason']
        except(KeyError, AttributeError)as e:
            reason = " "

        try:
           number_of_days =  request.data['number_of_days']
        except(KeyError, AttributeError)as e:
            number_of_days = None

        try:
           type_of_leave =  request.data['type_of_leave']
        except(KeyError, AttributeError)as e:
            type_of_leave = None

        try:
           leave_from =  request.data['leave_from']
        except(KeyError, AttributeError)as e:
            leave_from = None

        try:
           to_leave =  request.data['to_leave']
        except(KeyError, AttributeError)as e:
            to_leave = None

        if user:
            try:
                apply_leave_instance = AppliedLeave(
                    user=user,
                    type_of_leave=type_of_leave,
                    leave_from=leave_from,
                    to_leave=to_leave,
                    number_of_days=number_of_days,
                    reason = reason,
                    appliedBy=user
                )
                apply_leave_instance.save()
            except(KeyError, AttributeError, TypeError)as e:
                pass
            return JsonResponse({'message': 'Leave Applied Successfully'}, status=200)
        return JsonResponse({'message': 'User Not Found'}, status=405)
    return JsonResponse({'message': 'Bad Request'}, status=400)


def update_balance_leave(user, typeOfLeave, days):
    leave = Leaves.objects.filter(user=user).first()
    leave_type = 'balance_' + typeOfLeave
    col_value = getattr(leave, leave_type)
    if col_value is not None:

        if leave_type == 'balance_compoff_leave':
            print('in balance compoff')
            bal = float(col_value) + float(days)
            updateLeaves = Leaves.objects.filter(user=user).update(**{leave_type: bal, 'total_compoff_leave': bal})
            message = 1
        else:
            bal = float(col_value) - float(days)
            if bal<0:
                updateLeaves = Leaves.objects.filter(user=user).update(**{leave_type: 0})
                bal = abs(bal)
                print(bal)
                lop_add = EmployeeLop(
                    user = user,
                    count = bal
                    )
                lop_add.save()
            else:
                updateLeaves = Leaves.objects.filter(user=user).update(**{leave_type: bal})
            message = 1
    else:
        message = 2
    return message


@api_view(['PUT'])
def approve_leave(request):
    applied_leave = get_object_or_None(AppliedLeave, id=request.data['leave_id'], status=False, declined=False)
    user = get_object_or_None(User, id=request.data['user'])
    if user:
        if applied_leave:
            applied_leave.status = request.data['approval_status']
            if applied_leave.status:
                applied_leave.approvedBy = user
                applied_leave.approvedOn = timezone.now()
            applied_leave.actionOn = timezone.now()

            if applied_leave.status:
                # leave_bal = Leaves.objects.get(user=applied_leave.appliedBy)
                updating_leave = update_balance_leave(applied_leave.appliedBy, applied_leave.type_of_leave,
                                                      applied_leave.number_of_days)
                if updating_leave == 1:
                    applied_leave.save()
                    return JsonResponse({'message': 'Approve Leave and Updated Balance Leave'}, status=204)
                elif updating_leave == 2:
                    return JsonResponse({'message': 'Invalid Leave'}, status=400)
            else:
                applied_leave.declined = True
                applied_leave.save()
                return JsonResponse({'message': 'Leave Application Declined'}, status=200)
        else:
            return JsonResponse({"message": "Either Leave is Invalid Or Leave Expired"}, status=400)
    else:
        return JsonResponse({"message": "Unauthorized User"}, status=403)





class ManagerLeaveView(APIView):    
    def get(self, request):
        if request.user.user_role.role_type == 'Manager':
            user_list = Role.objects.filter(department=request.user.user_role.department)
            user_ids = [i.user_id for i in user_list]
            applied_leave = AppliedLeave.objects.filter(appliedBy__in=user_ids)
            appliedLeaveUsers = [i.user_id for i in applied_leave]
            print(appliedLeaveUsers)
            leaves = User.objects.filter(id__in=appliedLeaveUsers)
            serializer = EmployeesLeaveForManager(leaves, many=True)
            return Response(serializer.data)
        return JsonResponse({'message':'Unauthorized Access'})

##############-------------------------HR Payrole----------------------####################

class HrUserView(APIView):
    def get(self, request, format=None):
        if request.user.user_role.department == 'HR':
            employees = Role.objects.all()
            user_ids = [i.user_id for i in employees]
            users = User.objects.filter(id__in=user_ids)
            serializer = HrUserSerializer(users, many=True)
            return Response(serializer.data)


class SalaryView(APIView):
    def post(self, request, format=None):
        if request.data:
            serializer = SalarySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Saved Salary of the Employee'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        salary = Salary.objects.all()
        serializer = SalarySerializer(salary, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        if request.data:
            salary = Salary.objects.filter(user=request.data['user']).first()
            if salary:
                serializer = SalarySerializer(salary, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Updated Salary of the employee'}, status=200)
                return JsonResponse({'message':'Bad String'}, status=400)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request, format=None):
        if request.data:
            salary = Salary.objects.filter(user=request.data['user']).first()
            if salary:
                salary.delete()
                return JsonResponse({'message':'Salary Deleted Successfully'}, status=200)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad String'}, status=400)


##############-------------------------Employee Document----------------------###################
class EmployeeDocumentView(APIView):
    def post(self, request):
        if request.data:
            serializer = EmployeeDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return  JsonResponse({'message':'Document Uploaded Successfully'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)


    def get(self, request):
        documents = EmployeeDocument.objects.all()
        serializer = EmployeeDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def put(self, request):
        if request.data:
            try:
                document = EmployeeDocument.objects.get(id = request.data['id'])
                if document:
                    serializer = EmployeeDocumentSerializer(document, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'message':'Document Updated Successfully'}, status=200)
                    return JsonResponse({'message':'Bad String'}, status=400)
                return JsonResponse({'message':'Not Found'}, status=400)
            except(ObjectDoesNotExist)as e:
                return JsonResponse({'message':'Requested Document details Does Not Exist'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request):
        if request.data:
            try:
                document = EmployeeDocument.objects.get(id = request.data['id'])
                if document:
                    document.delete()
                    return JsonResponse({'message': 'Document Deleted Successfully'}, status=400)
                return JsonResponse({'message':'Not Found'}, status=400)
            except(ObjectDoesNotExist)as e:
                return JsonResponse({'message':'Request Document Does Not Exist'}, status=400)
        return JsonResponse({'message': 'Bad Request'}, status=400)


class EmployeeDocumentIndividual(APIView):
    def get(self, request, user):
        documents = EmployeeDocument.objects.filter(user=user)
        serializer = EmployeeDocumentSerializer(documents, many=True)
        return Response(serializer.data)

##############-------------------------HR Payrole----------------------####################


class HrUserListView(APIView):
    def get(self, request, format=None):
        if request.user.user_role.department == 'HR':
            employees = Role.objects.all()
            user_ids = [i.user_id for i in employees]
            users = User.objects.filter(id__in=user_ids)
            serializer = HrUserSerializer(users, many=True)
            return Response(serializer.data)
        return JsonResponse({'message':'Unauthorised user'}, status=401)

class HrUsersDetailsView(APIView):
    def get(self, request, user, format=None):
        print(user)
        if request.user.user_role.department == 'HR':
            user_obj = User.objects.filter(id=user)
            serializer = HrUserDetailSerializer(user_obj)
            print(serializer)
            return Response(serializer.data)
        return JsonResponse({'message':'Unauthorised user'}, status=401)
            

class SalaryView(APIView):
    def post(self, request, format=None):
        if request.data:
            serializer = SalarySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Saved Salary of the Employee'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        salary = Salary.objects.all()
        serializer = SalarySerializer(salary, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        if request.data:
            salary = Salary.objects.filter(user=request.data['user']).first()
            if salary:
                serializer = SalarySerializer(salary, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Updated Salary of the employee'}, status=200)
                return JsonResponse({'message':'Bad String'}, status=400)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request, format=None):
        if request.data:
            salary = Salary.objects.filter(user=request.data['user']).first()
            if salary:
                salary.delete()
                return JsonResponse({'message':'Salary Deleted Successfully'}, status=200)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad String'}, status=400)


class SalaryIndividual(APIView):
    def get(self, request, user):
        salary = Salary.objects.get(user=user)
        serializer = SalarySerializer(salary)
        return Response(serializer.data)


############------------Bank Details-----------------################
class BankDetailsView(APIView):
    def post(self, request):
        if request.data:
            serializer = BankDetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Bank Details Of Employee Added Successfully'}, status=201)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request):
        bankDetails = BankDetails.objects.all()
        serializer = BankDetailsSerializer(bankDetails, many=True)
        return Response(serializer.data)

    def put(self, request):
        if request.data:
            try:
                _id = request.data['id']
            except(KeyError)as e:
                return JsonResponse({'message':'Unique Id Required'}, status=400)
            bankDetails = BankDetails.objects.get(id=_id)
            serializer = BankDetailsSerializer(bankDetails, data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Bank Details Updated Successfully'}, status=200)
            return Response(serializer.errors)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request):
        if request.data:
            try:
                _id = request.data['id']
            except(KeyError)as e:
                return  JsonResponse({'message':'Unique Id Required'}, status=400)
            bankDetails = BankDetails.objects.get(id=_id)
            if bankDetails:
                bankDetails.delete()
                return JsonResponse({'message':'Bank Details Deleted Successfully'}, status=200)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

class BankDetailsIndividual(APIView):
    def get(self, request, user):
        bankDetails = BankDetails.objects.get(user = user)
        serializer = BankDetailsSerializer(bankDetails)
        return Response(serializer.data)


#############----------------Salary Request-------------##################
@api_view(['POST'])
def salary_request(request):
    user_id = request.data.get('user', None)
    month = request.data.get('month', None)
    year = request.data.get('year', None)
    if user_id:
        salary_info = Salary.objects.filter(user=user_id).first()
        calculate_lop = calculate_lop_f(user_id, month, year)
        salary_of_one_day = float(salary_info.net_salary)/float(25)
        lop_cost = float(calculate_lop)*float(salary_of_one_day)
        salary_request=SalaryRequest(
                user = salary_info.user,
                basic = salary_info.basic,
                hra = salary_info.hra,
                conveyance_allowance = salary_info.conveyance_allowance,
                deduction = lop_cost,
                misc_allowance = salary_info.misc_allowance,
                proffesional_tax = salary_info.proffesional_tax,
                net_salary = salary_info.net_salary
            )
        salary_request.save()
        return JsonResponse({'message':'Salary Requested'}, status=200)
    return JsonResponse({'message':'Bad Request'}, status=400)


def calculate_lop_f(user_id, month, year):
    employee_lop = EmployeeLop.objects.filter(user=user_id, appliedOn__month=month, appliedOn__year=year, status=True).all()
    print(employee_lop)
    lop = 0
    if employee_lop:
        for e in employee_lop:
            lop += e.count
            e.status=False
            e.save()
        return lop
    return lop

######----------Credit Salary--------######
class SalaryRequested(APIView):
    def get(self, request):
        salaries = SalaryRequest.objects.filter(credited=False).all()
        serializer = SalaryRequestedSerializer(salaries, many=True)
        return Response(serializer.data)

    def put(self, request):
        if request.data:
            _id = request.data.get('id', None)
            if _id:
                requested_salary = SalaryRequest.objects.filter(id=_id).first()
                serializer = SalaryRequestPutSerializer(requested_salary, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Requested Salary updated successfully'}, status=200)
                return Response(serializer.errors)
            return JsonResponse({'message':'Unique Id Required to identify requested salary'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)


#######--------Salary Credited--------##########
@api_view(['POST'])
def salary_credited(request):
    if request.data:
        _id = request.data.get('id', None)
        user_id = request.data.get('user', None)
        if _id and user_id:
            salary = SalaryRequest.objects.filter(id= _id, user=user_id, credited=False).first()
            if salary:
                salary.credited_on = timezone.localtime(timezone.now())
                salary.credited = True
                salary.save()
                return JsonResponse({'message':'Salary Request status changed to Creadited'}, status=200)
            return JsonResponse({'message':'Not Found, Invalid data'}, status=400)
        return JsonResponse({'message':'unique id and user id is neccessory'}, status=400)
    return JsonResponse({'message':'Bad Request'}, status=400)
