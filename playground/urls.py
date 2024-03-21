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
    path('dashboard_student/', views.dashboard, name='dashboard_student'),
    path('dashboard_mentor/', views.dashboard, name='dashboard_mentor'),
    path('accounts/logout/', LogoutView.as_view(template_name='logout.html'), name='logout_page'),
    path('create-classroom',views.createClassroom, name='create-classroom'),
    path('classrooom/<str:pk>/',views.classroom,name='classroom'),
    path('classroom/<str:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('classroom/<str:classroom_id>/create-test/', views.create_test, name='create-test'),
    path('classroom/<int:pk>/take-test/<int:test_id>/', views.take_test, name='take_test'),
    path('classroom/<int:pk>/take-test/<int:test_id>/<int:question_index>/', views.take_test, name='take_test'),
]