from django.db import models
from django.contrib.auth.hashers import make_password

class Parent(models.Model):
    guardian_id = models.CharField(max_length=20, unique=True)
    registration_date = models.DateField()
    father_name = models.CharField(max_length=100)
    father_qualification = models.CharField(max_length=100, blank=True)
    father_designation = models.CharField(max_length=100, blank=True)
    father_office_address = models.TextField(blank=True)
    father_phone = models.CharField(max_length=15, blank=True)
    father_email = models.EmailField(blank=True)
    father_aadhaar = models.CharField(max_length=12, blank=True)
    father_signature = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100)
    mother_qualification = models.CharField(max_length=100, blank=True)
    mother_designation = models.CharField(max_length=100, blank=True)
    mother_office_address = models.TextField(blank=True)
    mother_phone = models.CharField(max_length=15, blank=True)
    mother_email = models.EmailField(blank=True)
    mother_aadhaar = models.CharField(max_length=12, blank=True)
    mother_signature = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(default=False)  # New


    def __str__(self):
        student_names = ", ".join([s.name for s in self.students.all()]) or "No Student"
        return f"{self.father_name} & {self.mother_name} (Student: {student_names})"


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=100, default='Unknown')
    std = models.CharField(max_length=100, default='Unknown')
    division = models.CharField(max_length=5, default='A')
    address = models.CharField(max_length=255, default='Unknown')
    age = models.PositiveIntegerField(default=18)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=128)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    guardian_email = models.EmailField(blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='student_profiles/', null=True, blank=True)
    parent = models.ForeignKey('Parent', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.std} - {self.division})"

    def save(self, *args, **kwargs):
        # Hash password only if not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
