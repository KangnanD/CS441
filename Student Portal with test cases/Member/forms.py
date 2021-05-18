from django import forms
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget, AdminTextareaWidget, AdminFileWidget
from django.contrib.auth import password_validation
from django.contrib.auth.models import Group
from django.forms import SelectDateWidget

from Member.models import Member, Post, Jira, File, Comment, Role, Course, FileType
from django.conf import settings
import re


class MemberRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(widget=forms.TextInput())
    role = forms.ChoiceField(choices=Member.ROLE_CHOICES, widget=forms.Select())
    accept = forms.BooleanField(required=True, label="<a href='/guidelines/'>Agree with guidelines</a>")

    class Meta():
        model = Member
        fields = ('username', 'email', 'password', 'role', 'accept')

    def is_valid(self):
        if super().is_valid():
            if re.match(settings.STUDENT_EMAIL_REGEX, self.cleaned_data['email']):
                return super(MemberRegisterForm, self).is_valid()
            else:
                self._errors['email'] = ["Please Enter a Valid Email Address."]
                return False
        else:
            return False


class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('first_name','last_name','email','image','accept')

    def is_valid(self):
        if super().is_valid():
            return True
        else:
            return False


class MemberLoginForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }


class MemberPasswordChangeForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ('The two password fields didn’t match.'),
        'password_incorrect': ("Your old password was entered incorrectly. Please enter it again."),
    }

    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.member.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def __init__(self, member, *args, **kwargs):
        self.member = member
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.set_password(password)
        if commit:
            self.save()
        return self

    class Meta():
        model = Member
        widgets = {
            'old_password': forms.PasswordInput(),
            'new_password1': forms.PasswordInput(),
            'new_password2': forms.PasswordInput()
        }
        fields = ('old_password', 'new_password1', 'new_password2')


class MemberPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content','member', 'course')
        error_messages = {
            'member': {
                'invalid_choice': "Post Member Error Message.",
            },
            'file_type': {
                'invalid_choice': "Post FileType Error Message.",
            },
            'course': {
                'invalid_choice': "Post Course Error Message.",
            },
            'file': {
                'required': "Post File Error Message."
            }
        }


class MemberPostFormWithFiles(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'file', 'file_type', 'member', 'course')
        error_messages = {
            'member': {
                'invalid_choice': "Post Member Error Message.",
            },
            'file_type': {
                'invalid_choice': "Post FileType Error Message.",
            },
            'course': {
                'invalid_choice': "Post Course Error Message.",
            },
            'file': {
                'required': "Post File Error Message."
            }
        }


class JiraCreateForm(forms.ModelForm):
    description = forms.CharField(widget=AdminTextareaWidget())
    due_at = forms.DateField(widget=AdminDateWidget())
    #files = forms.FileField(widget=forms.FileInput(attrs={'multiple': True, 'class': "dropzone", 'action': "/files/upload/"}))
    reporter = forms.HiddenInput()

    class Meta:
        model = Jira
        fields = ('type','title', 'description', 'due_at', 'course', 'reporter','assignee', 'status')

    def save_files(self, files):
        files_list = []
        for file in files:
            f = File()
            f.name = file.name
            f.file = file
            f.save()
            files_list.append(f)
        return files_list

    def is_valid(self):
        if super().is_valid():
            return True
        else:
            return False


class CommentCreateForm(forms.ModelForm):
    text = forms.CharField(widget=AdminTextareaWidget())

    class Meta:
        model = Comment
        fields = ('text',)

    def is_valid(self):
        if super().is_valid():
            return True
        else:
            return False


class FileCreateForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': "dropzone", 'url': "/files/upload/"}))

    class Meta:
        model = File
        fields = ('file',)

    def is_valid(self):
        if super().is_valid():
            return True
        else:
            return False


class AddStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = self.request.member.courses
        self.fields['member'].queryset = Member.objects.filter(role=Role.STUDENT.name)

    class Meta:
        model = Post
        fields = ('member','course',)

    def is_valid(self):
        return True


class RemoveStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(RemoveStudentForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = self.request.member.courses
        self.fields['member'].queryset = Member.objects.filter(role=Role.STUDENT.name)

    class Meta:
        model = Post
        fields = ('member','course',)

    def is_valid(self):
        return True


class LinkJiraForm(forms.ModelForm):
    links = forms.ModelChoiceField(queryset=Jira.objects.all())

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(LinkJiraForm, self).__init__(*args, **kwargs)
        self.fields['links'].queryset = Jira.objects.all()

    class Meta:
        model = Jira
        fields = ('links',)

    def is_valid(self):
        return True
