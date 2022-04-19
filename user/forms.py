from django import forms
from .models import User
from .models import user_profile

class Userupdateform (forms.ModelForm):

    class Meta:
        model = User
        fields = ('email','first_name','last_name' )

class Proupdateform (forms.ModelForm):

    class Meta:
        model = user_profile
        fields = ('image', )