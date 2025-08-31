from django.db import models
from django.contrib.auth.hashers import make_password


class Teacher(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    subject = models.CharField(max_length=100)
    std = models.CharField(max_length=20, blank=True, null=True)
    division = models.CharField(max_length=5)
    qualification = models.CharField(max_length=150, blank=True)
    experience = models.PositiveIntegerField(default=0, help_text="Years of teaching experience")
    joining_date = models.DateField(auto_now_add=True)
    teacher_id = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='teacher_profiles/', blank=True, null=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)  # New field


    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.subject})"


class Diary(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    file = models.FileField(upload_to='diary_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # New field

    def __str__(self):
        return self.title


class Alert(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # New field


    def __str__(self):
        return self.title


class Performance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)  # Consider changing to ForeignKey to Student for data integrity
    subject = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    remarks = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)  # New field


    def __str__(self):
        return f"{self.student_name} - {self.subject}"


class Message(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)  # Could be ForeignKey to Parent for integrity
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"{self.parent_name} - {self.teacher.name}"


class Event(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # New field

    def __str__(self):
        return self.title


class Feedback(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)  # Consider ForeignKey to Student
    feedback = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.student_name}"


class Report(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    report_file = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # New field

    def __str__(self):
        return self.title
