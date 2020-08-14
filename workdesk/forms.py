from django import forms
from .models import WorkProject


class AddProject(forms.ModelForm):
    class Meta:
        model = WorkProject
        exclude = ('status', 'owner',)

    def clean_owner(self):
        owner = self.instance.user
        print(owner)
        return owner

    def save(self, commit=True):
        self.instance.owner = self.request.user
        return super().save(commit=commit)


class UpdateProject(forms.ModelForm):
    class Meta:
        model = WorkProject
        exclude = ('owner',)

    def clean_owner(self):
        owner = self.instance.user
        print(owner)
        return owner

    def save(self, commit=True):
        return super().save(commit=commit)
