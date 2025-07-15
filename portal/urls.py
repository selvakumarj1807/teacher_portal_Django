from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view),
    path('home/', views.home, name='home'),
    path('add_student/', views.add_or_update_student),
    path('edit_student/<int:student_id>/', views.edit_student),
    path('delete_student/<int:student_id>/', views.delete_student),
]
