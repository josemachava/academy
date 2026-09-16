from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]
    title = models.CharField(max_length=255)
    instructor = models.CharField(max_length=150, default="Academy Team")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    reviews = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=50, default="6h 00m")
    students = models.CharField(max_length=50, default="1.0k")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner")
    tags = models.CharField(max_length=255, default="", blank=True)
    category = models.CharField(max_length=100, default="Development")
    extra_tags = models.PositiveIntegerField(default=0)
    role = models.CharField(max_length=150, default="Teacher")
    lessons = models.PositiveIntegerField(default=10)
    emoji = models.CharField(max_length=10, default="📚")
    is_new = models.BooleanField(default=False)
    staff_pick = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("enrolled", "Enrolled"),
        ("completed", "Completed"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="enrolled")
    progress = models.PositiveIntegerField(default=0)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user} -> {self.course} ({self.status})"


class SavedCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="saved_by")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user} saved {self.course}"
