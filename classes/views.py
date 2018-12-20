from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Classroom , Student
from .forms import ClassroomForm , SignupForm , SigninForm , studentForm
from django.contrib.auth import login, authenticate , logout 

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)

def signup(request):
        form = SignupForm()
        if request.method == 'POST':
          form = SignupForm(request.POST)
          if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            # Where you want to go after a successful signup
            return redirect("classroom-list")
        context = {"form":form,}
        return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                # Where you want to go after a successful login
                return redirect('classroom-list')

    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    
     logout(request)
     return redirect("signin") 

def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	students = Student.objects.filter(classroom=classroom).order_by('name','-exam_grade')
	context = {
		"classroom": classroom,
		"students": students,

	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if request.user.is_anonymous:
		return redirect('signin')
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			class_obj =form.save(commit = False)
			class_obj.teacher=request.user
			class_obj.save()
			#form.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)

def add_student(request ,classroom_id):
	form = studentForm()
	class_obj = Classroom.objects.get(id=classroom_id)
	if request.method == "POST":
		form = studentForm(request.POST, request.FILES or None)
		if form.is_valid():
			student_obj = form.save(commit = False)
			student_obj.classroom = class_obj
			student_obj.save()
			#form.save()
			messages.success(request, "Successfully add!")
			return redirect('classroom-detail',classroom_id) 
		print (form.errors)
	context = {
	"form": form,
	"class_obj":class_obj,
	}
	return render(request, 'addstudent.html', context)

def student_update(request, classroom_id,student_id):
	classroom = Classroom.objects.get(id=classroom_id)
	student = Student.objects.get(id=student_id)
	form = studentForm(instance=student)
	if request.method == "POST":
		form = studentForm( request.POST, request.FILES or None, instance=student)
		if form.is_valid():
			#student_obj = form.save(commit = False)
			#student_obj.classroom = class_obj
			#student_obj.save()
			form.save()
			messages.success(request, "Successfully update!")
			return redirect('classroom-detail',classroom_id) 
	context = {
	"form": form,
	"student":student,
	"classroom":classroom,
	}
	return render(request, 'student_update.html', context)

def student_delete(request,classroom_id ,student_id):
	Student.objects.get(id=student_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-detail',classroom_id)

def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')
