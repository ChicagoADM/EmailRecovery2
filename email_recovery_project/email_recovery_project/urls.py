from django.contrib import admin
from django.urls import path
from email_form import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.create_email_request, name='create_request'),
    path('success/<str:request_number>/', views.success_view, name='success'),
]