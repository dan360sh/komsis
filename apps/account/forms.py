import re
from django import forms
from django.forms import ValidationError
from apps.account.models import Account


def validate_password(value):
    password_pattern = r'^[A-z0-9]{6,100}$'
    if not re.match(password_pattern, value):
        raise ValidationError(
            "Пароль должен быть размером от 6 символов и состоять из " +
            "латинских букв и цифр", code="invalid_password")


class LoginForm(forms.Form):
    """Форма входа в личный кабинет"""

    email = forms.EmailField(
        required=True, error_messages={'required': "Введите Email"})
    password = forms.CharField(
        required=True, widget=forms.PasswordInput(),
        error_messages={'required': "Введите пароль"})


class RegisterForm(forms.Form):
    """Форма регистрации в личном кабинете"""

    name = forms.CharField(
        required=True, error_messages={'required': 'Введите имя'})
    surname = forms.CharField(
        required=True, error_messages={'required': 'Введите фамилию'})
    middle_name = forms.CharField(required=False)
    email = forms.EmailField(
        required=True, error_messages={'required': 'Введите email'})
    phone = forms.CharField(
        required=True, error_messages={'required': 'Введите номер телефона'})
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False), required=True,
        error_messages={'required': "Введите пароль"},
        validators=[validate_password])
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(render_value=False), required=True,
        error_messages={'required': "Повторите пароль"})
    jurical = forms.BooleanField(required=False)
    company_title = forms.CharField(
        required=False,
        error_messages={'required': "Введите наименование компании"})
    company_inn = forms.CharField(
        required=False,
        error_messages={'required': "Введите ИНН компании"})
    acceptance = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'Подтвердите согласие на обработку данных'})

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        jurical = cleaned_data.get('jurical', None)
        if jurical:
            cleaned_data['jurical'] = True
        return cleaned_data

    class Meta:
        error_messages = {
            'acceptance': {
                'required': 'Подтвердте согласие на обработку данных',
            }
        }


class ChangePasswordForm(forms.Form):
    """Форма смены пароля пользователя Django"""

    old_password = forms.CharField(
        widget=forms.PasswordInput(render_value=False), required=True,
        error_messages={'required': "Введите старый пароль"})
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False), required=True,
        error_messages={'required': "Введите новый пароль"},
        validators=[validate_password])
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(render_value=False), required=True,
        error_messages={'required': "Повторите пароль"})

    def is_valid(self):
        valid = super(ChangePasswordForm, self).is_valid()
        if valid:
            if self.cleaned_data['password'] != \
                    self.cleaned_data['password_repeat']:
                self.errors['password_repeat'] = ["Пароли не совпадают", ]
                return False
        return valid
