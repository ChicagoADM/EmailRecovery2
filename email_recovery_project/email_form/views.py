from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import EmailRequestForm
from .models import EmailRequest

def create_email_request(request):
    if request.method == 'POST':
        form = EmailRequestForm(request.POST)
        if form.is_valid():
            # Сохраняем заявку
            email_request = form.save()
            
            # Получаем отображаемое название действия
            action_display = email_request.get_action_display()
            
            # Отправляем email
            subject = f'Заявка на {action_display} почты ЕПС №{email_request.request_number}'
            
            # Формируем тело письма
            message_body = render_to_string('email_form/email_template.txt', {
                'request': email_request
            })
            
            try:
                send_mail(
                    subject,
                    message_body,
                    settings.DEFAULT_FROM_EMAIL,
                    ['gkb29-IT@zdrav.mos.ru'],
                    fail_silently=False,
                )
                email_request.is_sent = True
                email_request.save()
                messages.success(request, f'Заявка на {action_display} №{email_request.request_number} успешно отправлена!')
            except Exception as e:
                messages.error(request, f'Ошибка при отправке email: {str(e)}')
            
            return redirect('success', request_number=email_request.request_number)
    else:
        form = EmailRequestForm()
    
    return render(request, 'email_form/form.html', {'form': form})

def success_view(request, request_number):
    return render(request, 'email_form/success.html', {'request_number': request_number})

def success_view(request, request_number):
    # Получаем заявку по номеру
    email_request = EmailRequest.objects.get(request_number=request_number)
    return render(request, 'email_form/success.html', {
        'request_number': request_number,
        'phone': email_request.phone  # Передаем номер телефона из заявки
    })