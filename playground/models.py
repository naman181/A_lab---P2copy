from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .managers import CustomUserManager
from django.conf import settings
from django.db import models
import uuid

class CustomUser(AbstractUser):
    STUDENT = 'student'
    MENTOR = 'mentor'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (MENTOR, 'Mentor'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
    )
    username = models.CharField(max_length=40, unique=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)  # made first name optional
    last_name = models.CharField(max_length=30, blank=True)   # made last name optional
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='user_set', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='user_set', related_query_name='user')

    def __str__(self):
        return self.email

class Student(CustomUser):
    def __str__(self):
        return f"{self.first_name} {self.last_name} (Student)"

class Mentor(CustomUser):
    def __str__(self):
        return f"{self.first_name} {self.last_name} (Mentor)"

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'

    CLASSROOM_TYPE_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    )
    classroom_type = models.CharField(
        max_length=10,
        choices=CLASSROOM_TYPE_CHOICES,
        default=PUBLIC,
    )
    # host = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='hosted_classrooms', limit_choices_to={'role': 'mentor'})
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(CustomUser, related_name='participants', blank=True) 
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Test(models.Model):
    # mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    # mentor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='hosted_classrooms', limit_choices_to={'role': 'mentor'})
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    time_limit_per_question = models.PositiveIntegerField(default=60)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return self.question_text

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']  # Changed the ordering to descending

    def __str__(self):
        return self.body[:50]

class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']  # Changed the ordering to descending


class TestScore(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='testscore_student', limit_choices_to={'role': 'student'})
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'test')
        ordering = ['-timestamp']

class QuestionResponse(models.Model):
    test_score = models.ForeignKey(TestScore, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    time_taken = models.PositiveIntegerField(default=0)  # Time taken to answer the question in seconds

class TestAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.end_time is not None and self.start_time > self.end_time:
            raise ValueError("End time must be after start time.")
        super().save(*args, **kwargs)

class TestAttemptQuestion(models.Model):
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], null=True)
    time_taken = models.PositiveIntegerField(default=0)  # Time taken to answer the question in seconds
