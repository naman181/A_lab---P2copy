from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Topic, Message, Enrollment, Test, Classroom, Student, Mentor, Question, TestScore, TestAttempt, QuestionResponse,TestAttemptQuestion  # Import your custom user model

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()

# Register the custom user model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Enrollment)
admin.site.register(Test)
admin.site.register(Classroom)

# admin.site.register(Student)
# admin.site.register(Mentor)

admin.site.register(Question)
admin.site.register(TestScore)
admin.site.register(QuestionResponse)
admin.site.register(TestAttemptQuestion)
# admin.site.register(TestAttempt)

