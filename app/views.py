from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import QueryDict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Patient,Doctor,Address




def home(request):
	if request.method == "GET":
		if request.user.is_authenticated:
			patient = Patient.objects.filter(user=request.user).last()
			context={}
			if patient:
				context["patient"] = patient
				return render(request,"patient_homepage.html",context)
			else:
				doctor = Doctor.objects.filter(user=request.user).last()
				context["doctor"] = doctor
				return render(request,"doctor_homepage.html",context)

		return redirect("signin")

def signin(request):
	if request.method == "GET":
		return render(request,'signin.html')
	elif request.method == "POST":
		email = request.POST.get("email")
		password = request.POST.get("password")

		if not email:
			return JsonResponse({"error":"no email found"},status=400)
		if not password:
			return JsonResponse({"error":"no password found"},status=400)

		uname = authenticate(username=email,password=password)
		if not uname:
			return JsonResponse({"error":"authentication failed!"})
		login(request,uname)
		return JsonResponse({"msg":"sign in successfull"},status=200)

def signup(request):
	if request.method == "GET":
		return render(request,'signup.html')
	elif request.method == "POST":
		print(request.POST)
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		password = request.POST.get("password")
		confirm_password = request.POST.get("confirm_password")
		username = request.POST.get("username")
		profile_image = request.FILES.get("profile_image")
		email = request.POST.get("email")
		user_type = request.POST.get("user_type")

		print(profile_image)


		#address
		line1 = request.POST.get("line1")
		city = request.POST.get("city")
		state = request.POST.get("state")
		pincode = request.POST.get("pincode")

		if not first_name or first_name == "undefined":
			return JsonResponse({"error":"first name is a required field"},status=400)
		if not last_name or last_name == "undefined":
			return JsonResponse({"error":"last name is a required field"},status=400)
		if not password or password == "undefined":
			return JsonResponse({"error":"password is a required field"},status=400)
		if not confirm_password or confirm_password == "undefined":
			return JsonResponse({"error":"confirm password is a required field"},status=400)
		if not username or username == "undefined":
			return JsonResponse({"error":"username is a required field"},status=400)
		if not user_type or user_type == "undefined":
			return JsonResponse({"error":"username is a required field"},status=400)
		if not email or email == "undefined":
			return JsonResponse({"error":"email is a required field"},status=400)



		if password != confirm_password:
			return JsonResponse({"error":"password and confirm password is not same"},status=400)

		existng_user = User.objects.filter(username=email).last()
		if existng_user:
			return JsonResponse({"error":"already an existing email please log in "},status=400)


		main_obj = {}
		main_obj["username"] = username
		main_obj["profile_pic"] = profile_image


		user_obj = {
                    "username": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_active": True,
            }
		address_obj = {
            		"line1":line1,
            		"city":city,
            		"state":state,
            		"pincode":pincode
            }           
		user = User.objects.create(**user_obj)
		address = Address.objects.create(**address_obj)
		user.set_password(password)
		user.save()

		if user_type == "patient":
			Patient.objects.create(user=user,address=address,**main_obj)
			login(request,user)
			return JsonResponse({"msg":"created patient successfully"},status=200)


		elif user_type == "doctor":
			Doctor.objects.create(user=user,address=address,**main_obj)
			login(request,user)
			return JsonResponse({"msg":"created doctor successfully"},status=200)

		return JsonResponse({"error":"something happened, please try again"},status=400)


def logout_account(request):
	logout(request)
	return redirect("home")



