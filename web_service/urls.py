from django.conf.urls import url
from . import views
 

urlpatterns=[
	url(r'^register/', views.register, name='register'),
	url(r'userLogin', views.login, name='userlogin'),
	url(r'^logout/$', views.logout, name='logout'),
	
	#url(r'^attendance/', views.AttendanceCreate.as_view()),

	url(r'^forgot_password$', views.forgot_password, name='forgot_password'),

	url(r'^add_employee', views.AddEmployeeView.as_view(), name='add_employee'),

	url(r'^approve_employee', views.ApproveEmployee.as_view(), name='approve_employee'),

	###########Salary################
	url(r'^salary_credited$', views.salary_credited, name='salary_credited'),
	url(r'^salary_request$', views.salary_request, name='salary_request'),
	url(r'^salary_requested$', views.SalaryRequested.as_view(), name='salary_requested'),
	url(r'^salary/(?P<user>[0-9]+)$', views.SalaryIndividual.as_view(), name='individual_salary'),
	url(r'^salary', views.SalaryView.as_view(), name='salary'),



	###########Bank Details###########
	url(r'^bank_details/(?P<user>[0-9]+)', views.BankDetailsIndividual.as_view(), name='individual_bank_details'),
	url(r'^bank_details', views.BankDetailsView.as_view(), name='bank_details'),


	###########HR API for user details#######
	url(r'^hr/user_list/all$', views.HrUserListView.as_view(), name='user_list_hr'),
	url(r'^hr/user_details/(?P<user>[0-9]+)', views.HrUsersDetailsView.as_view(), name='user_details_hr'),


	##############Employee Document################
	url(r'^employee/document$', views.EmployeeDocumentView.as_view(), name='employee_document'),
	url(r'^employee/document/(?P<user>[0-9]+)$', views.EmployeeDocumentIndividual.as_view(), name='employee_document_individual'),



	url(r'^holidays$', views.HolidayView.as_view(), name='holidays'),
	url(r'^leave/apply$', views.apply_leave, name='apply_leave'),
	url(r'^leaves$', views.MainLeaveView.as_view(), name='leave_assign'),
	url(r'^leaves/applied$', views.AppliedLeaveViewAPI.as_view(), name='applied_leaves'),
	url(r'^leave/approve$', views.approve_leave, name='leave_approve'),
	url(r'^leave/history/(?P<user_id>[0-9]+)', views.AppliedLeaveUserHistory.as_view(), name="leave_histody"),
	url(r'^leave/balance/(?P<user_id>[0-9]+)$', views.EmployeeBalanceLeave.as_view(), name='balance_leave'),
	url(r'^leave/info/(?P<user_id>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]+)$', views.LeaveUserInfo.as_view(), name='leave_info'),
	url(r'^leave/manager$', views.ManagerLeaveView.as_view(), name='leave_info_manager'),
]
