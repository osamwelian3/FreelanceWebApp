from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, WriterProfile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already taken")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("User with that username already exists")
        return username

    def clean_password2(self):
        # check if the two password entries match
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required fields, plus a repeated password
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username',)

    def clean_password2(self):
        # check if the two password entries match
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        # save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user,
    but replaces the password field with the admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'active', 'admin', )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RegisterWriterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already taken")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("User with that username already exists")
        return username

    def clean_password2(self):
        # check if the two password entries match
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2


ACADEMIC_CHOICES = (
        ('Accounting', 'Accounting'),
        ('Art & Architecture', 'Art & Architecture'),
        ('Chemistry', 'Chemistry'),
        ('Computer Science', 'Computer Science'),
        ('Family & Consumer', 'Family & Consumer'),
        ('History', 'History'),
        ('Science', 'Science'),
        ('Marketing', 'Marketing'),
        ('Music', 'Music'),
        ('Physics', 'Physics'),
        ('Religious Studies', 'Religious Studies'),
        ('Statistics', 'Statistics'),
        ('Women and Gender Studies', 'Women and Gender Studies'),
        ('Zoology', 'Zoology'),
        ('Anthropology', 'Anthropology'),
        ('Biology', 'Biology'),
        ('Classics', 'Classics'),
        ('Economics Education', 'Economics Education'),
        ('Film and Theatre Studies', 'Film and Theatre Studies'),
        ('Law', 'Law'),
        ('Mathematics', 'Mathematics'),
        ('Nursing', 'Nursing'),
        ('Political Science', 'Political Science'),
        ('Shakespeare', 'Shakespeare'),
        ('Technology', 'Technology'),
        ('World Affairs', 'World Affairs'),
        ('General', 'General'),
        ('Application Letters', 'Application Letters'),
        ('Business', 'Business'),
        ('Communications', 'Communications'),
        ('English Literature', 'English Literature'),
        ('Finance', 'Finance'),
        ('Management', 'Management'),
        ('Medicine', 'Medicine'),
        ('Philosophy', 'Philosophy'),
        ('Psychology', 'Psychology'),
        ('Sociology', 'Sociology'),
        ('Web, High tech', 'Web, High tech'),
        ('World literature', 'World literature'),
        ('Other', 'Other'),
    )

STYLE_CHOICES = (
        ('MLA', 'MLA'),
        ('APA', 'APA'),
        ('Chicago/Turabian', 'Chicago/Turabian'),
        ('HARVARD', 'Harvard'),
        ('Other', 'Other'),
    )


class WriterProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WriterProfileForm, self).__init__(*args, **kwargs)
        self.fields['academic_disciplines'].choices = ACADEMIC_CHOICES

    academic_disciplines = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'academic-list', 'style': 'width: 50px;'}),
        choices=ACADEMIC_CHOICES)
    styles = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'academic-list', 'style': 'width: 35px!important;'}),
        choices=STYLE_CHOICES)
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'placeholder': 'City'}))
    zip = forms.CharField(label='Zip/Postal Code', widget=forms.TextInput(attrs={'placeholder': 'Zip/Postal Code'}))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    native_language = forms.CharField(label='Your Native Language', widget=forms.TextInput(attrs={'placeholder': 'Your Native Language'}))
    brief_cv = forms.CharField(label='Your Brief CV', widget=forms.Textarea(attrs={'placeholder': 'Your Brief CV'}))
    certificate_title = forms.CharField(label='Give Your Certificate a title', widget=forms.TextInput(attrs={'placeholder': 'Give Your Certificate a Title'}))
    essay1_title = forms.CharField(label='Title for sample essay one',
                                        widget=forms.TextInput(attrs={'placeholder': 'Title for sample essay one'}))
    essay2_title = forms.CharField(label='Title for sample essay two',
                                   widget=forms.TextInput(attrs={'placeholder': 'Title for sample essay two'}))

    class Meta:
        model = WriterProfile
        exclude = ('user',)

    def clean_academic_disciplines(self):
        if len(self.cleaned_data['academic_disciplines']) > 5:
            raise forms.ValidationError('You cant choose more than five disciplines.')
        if len(self.cleaned_data['academic_disciplines']) < 1:
            raise forms.ValidationError('You must choose at least one discipline.')
        return self.cleaned_data['academic_disciplines']
