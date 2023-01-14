from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

def profile_image_path(instance, filename):
    folder_name = "profile_pics"
    return "/".join([folder_name, str(instance.id), filename])

class Address(models.Model):
	line1 = models.CharField(max_length=100,default="")
	city = models.CharField(max_length=100,default="")
	state = models.CharField(max_length=50,default="")
	pincode = models.CharField(max_length=6,default="")

class Patient(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to="patient_profiles", default="dummy.png")
	username = models.CharField(max_length=100)
	address = models.OneToOneField(Address,on_delete=models.CASCADE)
    
class Doctor(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to="doctor_profiles", default="dummy.png")
	username = models.CharField(max_length=100)
	address = models.OneToOneField(Address,on_delete=models.CASCADE)



   





