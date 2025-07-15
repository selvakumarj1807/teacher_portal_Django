from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Teacher, Student
import json

def login_view(request):
    if request.method == "POST":
        user = request.POST['username']
        pwd = request.POST['password']
        try:
            teacher = Teacher.objects.get(username=user, password=pwd)
            request.session['teacher_id'] = teacher.id
            return redirect('home')
        except Teacher.DoesNotExist:
            return HttpResponse("Invalid credentials")
    return render(request, "portal/login.html")

def home(request):
    if 'teacher_id' not in request.session:
        return redirect('login')
    students = Student.objects.all()
    return render(request, "portal/home.html", {"students": students})

@csrf_exempt
def add_or_update_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("DATA RECEIVED:", data)

        name = data.get('name')
        subject = data.get('subject')
        marks = data.get('marks')

        if not name or not subject or marks is None:
            return JsonResponse({'status': 'error', 'message': 'Missing field(s)'}, status=400)

        student, created = Student.objects.get_or_create(name=name, subject=subject)
        if not created:
            student.marks += int(marks)
        else:
            student.marks = int(marks)
        student.save()
        return JsonResponse({'status': 'added' if created else 'updated'})

@csrf_exempt
def edit_student(request, student_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            student = Student.objects.get(id=student_id)
            student.name = data['name']
            student.subject = data['subject']
            student.marks = int(data['marks'])
            student.save()
            return JsonResponse({'status': 'updated'})
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)

@csrf_exempt
def delete_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        return JsonResponse({'status': 'deleted'})
    except Student.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
