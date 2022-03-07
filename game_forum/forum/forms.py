from django import forms
from django.contrib.auth.forms import AuthenticationForm

# from forum.models import User
from django.contrib.auth.models import User
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField

from forum.models import Game, Developer, Company, Publisher, Sponsor, Award


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'price', 'description', 'image', 'genre')

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        # try:
        #     Developer.objects.get(game=)
        developer = ModelChoiceField(queryset=Company.objects.all())
        publisher = ModelChoiceField(queryset=Company.objects.all())
        sponsor = ModelChoiceField(queryset=Company.objects.all(), required=False, empty_label='None')
        award = ModelMultipleChoiceField(queryset=Award.objects.all(), required=False)
        self.fields['developer'] = developer
        self.fields['publisher'] = publisher
        self.fields['sponsor'] = sponsor
        self.fields['award'] = award
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AwardForm(ModelForm):
    class Meta:
        model = Award
        fields = ('name', 'description',)

    def __init__(self, *args, **kwargs):
        super(AwardForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class DeveloperForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name',)


class PublisherForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name',)


class SponsorForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name',)


class AuthUserForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AuthUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

