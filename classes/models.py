from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Classroom(models.Model):
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    year = models.IntegerField()
    teacher = models.ForeignKey(User,on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('classroom-detail', kwargs={'classroom_id':self.id})
        

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    exam_grade = models.IntegerField()
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
