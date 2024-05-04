from django.urls import path
from . import views
from django.contrib.auth import logout, login 
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from playground.views import login_page

urlpatterns = [
    path('landing_page/',views.landing_page,name='landing_page'),
    path('login_signup_page/', views.login_signup_page, name='login_signup_page'),
    path('registration/', views.registrationPage, name='registration'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout'),
    path('contact_page/',views.contact_page,name='contact_page'),
    path('faqs_page/',views.faqs_page,name='faqs_page'),
    path('learnmore_page/',views.learnmore_page,name='learnmore_page'),
    path('calander_page/',views.calander_page,name='calander_page'),
    path('dashboard_student/', views.dashboard, name='dashboard_student'),
    path('dashboard_mentor/', views.dashboard, name='dashboard_mentor'),
    path('profile_page/',views.profile_page,name='profile_page'),
    path('stuprofile_page/',views.stu_profile_page,name='stuprofile_page'),
    path('settings_page/',views.settings_page,name='settings_page'),
    path('stusettings_page/',views.stu_settings_page,name='stusettings_page'),
    path('history_page/',views.history_page,name='history_page'),
    path('genq_page/',views.genq_page,name='genq_page'),
    path('notification_page/',views.notification_page,name='notification_page'),
    path('stunotification_page/',views.stunotification_page,name='stunotification_page'),
    path('accounts/logout/', LogoutView.as_view(template_name='logout.html'), name='logout_page'),
    path('create-classroom',views.createClassroom, name='create-classroom'),
    path('classrooom/<str:pk>/',views.classroom,name='classroom'),
    path('classroom/<str:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('classroom/<str:classroom_id>/create-test/', views.create_test, name='create-test'),
    path('classroom/<int:pk>/show-test/<int:test_id>/', views.show_test, name='show_test'),
    path('classroom/<int:pk>/take-test/<int:test_id>/', views.take_test, name='take_test'),
    path('classroom/<int:pk>/take-test/<int:test_id>/<int:question_index>/', views.take_test, name='take_test'),
    path('classroom/<int:classroom_id>/student-report/<int:student_id>/', views.student_report, name='student_report'),

    path('test/<int:test_id>/report/', views.test_report, name='test_report'),
    path('test/<int:test_id>/report/download/', views.download_test_report_pdf, name='download_test_report_pdf'),
    path('download/', views.download_generated_responses, name='download_generated_responses'),
]
