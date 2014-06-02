from django.forms import *


class SignupForm(forms.Form):
    login = CharField(max_length=16)
    mail = EmailField()
    password = CharField(max_length=32, widget=PasswordInput)
    confirm_password = CharField(max_length=32, widget=PasswordInput)


class SigninForm(forms.Form):
    login = CharField(max_length=16)
    password = CharField(max_length=32, widget=PasswordInput)


class AskForm(forms.Form):
    title = CharField(max_length=32)
    text = CharField(max_length=2048, widget=Textarea({"class": "full_width"}))


class AnswerForm(forms.Form):
    text = CharField(max_length=2048, widget=Textarea({"class": "full_width"}))