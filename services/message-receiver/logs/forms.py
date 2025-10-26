from django import forms


class LogFilterForm(forms.Form):
    user_login = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        }),
        label='Username'
    )
    action = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All Actions'),
            ('register', 'Register'),
            ('login', 'Login'),
            ('login_failed', 'Failed Login'),
            ('logout', 'Logout'),
            ('send_message', 'Send Message'),
            ('send_message_failed', 'Failed Send Message'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Action Type'
    )
    start_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-select',
            'type': 'datetime-local'
        }),
        label='Start Date',
        input_formats=['%Y-%m-%dT%H']
    )
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label='End Date',
        input_formats=['%Y-%m-%dT%H']
    )