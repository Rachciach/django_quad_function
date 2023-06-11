from django.forms import ModelForm
from django import forms
from .models import QuadFunction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class QuadForm(ModelForm):
    class Meta:
        model = QuadFunction
        fields = ['example',"start_x", "end_x", "range_plot", "x1_range", "x2_range", "y1_range", "y2_range"]

# class QuadForm2(forms.Form):
#     example = forms.CharField()
#     start_x = forms.IntegerField()
#     end_x = forms.IntegerField()

class QuadForm2(ModelForm):
    class Meta:
        model = QuadFunction
        fields = ['example',"start_x", "end_x"]

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


