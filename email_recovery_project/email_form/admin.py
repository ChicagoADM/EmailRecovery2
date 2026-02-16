from django.contrib import admin
from .models import EmailRequest

@admin.register(EmailRequest)
class EmailRequestAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'action', 'last_name', 'first_name', 'created_at', 'is_sent']
    list_filter = ['action', 'is_sent', 'created_at']
    search_fields = ['request_number', 'last_name', 'first_name', 'current_email']
    readonly_fields = ['request_number', 'created_at']