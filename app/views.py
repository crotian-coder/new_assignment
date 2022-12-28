from django.shortcuts import render
from .models import User
from django.http import JsonResponse
from django.http import QueryDict

def home(request):
	if request.method == "GET":

		context = {}
		user = User.objects.all().last()

		if user:
			context["likes"] = user.likes 
			context["dislikes"] = user.dislikes
		else:
			User.objects.create(likes=0,dislikes=0)

		return render(request,'index.html',context=context)

	elif request.method == "PUT":
		put = QueryDict(request.body)
		dislikes = put.get("dislikes")
		likes = put.get("likes")

		context = {}

		user = User.objects.all().last()
		if likes:
			user.likes = user.likes + 1
			context["likes"] = user.likes

		if dislikes:
			user.dislikes = user.dislikes + 1
			context["dislikes"] = user.dislikes

		user.save()

		return JsonResponse(context)



