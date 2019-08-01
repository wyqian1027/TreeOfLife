from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Category, Hierarchy
# from tinymce.widgets import TinyMCE

        
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

class NewCatForm(ModelForm):

    # description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    # not working for whatever reason

    class Meta:
        model = Category
        fields = ("category_name", "category_parent", "hierarchy", "description", "image_address", "image_description")

    hierarchy = forms.ModelChoiceField(queryset=Hierarchy.objects.all(), required=True)
    category_parent = forms.ModelChoiceField(queryset=Category.objects.order_by('category_name'), required=True)


class NewCatFormByParent(ModelForm):

    # description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    # not working for whatever reason

    class Meta:
        model = Category
        fields = ("category_name", "hierarchy", "description", "image_address", "image_description")

    hierarchy = forms.ModelChoiceField(queryset=Hierarchy.objects.all(), required=True)
