from django import forms
from .models import EmailRequest

class EmailRequestForm(forms.ModelForm):
    class Meta:
        model = EmailRequest
        fields = [
            'action', 'reason', 'authority', 'institution',
            'last_name', 'first_name', 'patronymic',
            'department', 'position', 'phone',
            'address', 'building', 'office', 'current_email'
        ]
        widgets = {
            'action': forms.Select(attrs={'class': 'form-control', 'id': 'id_action'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'id_reason', 'required': True}),
            'authority': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'office': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'current_email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_current_email', 'required': True}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        reason = cleaned_data.get('reason')
        current_email = cleaned_data.get('current_email')
        
        if action in ['recovery', 'block']:
            if not reason:
                self.add_error('reason', 'Обязательное поле')
            if not current_email:
                self.add_error('current_email', 'Обязательное поле')
        
        return cleaned_data