from django import forms

from modules.core.models import Group, Tag
from modules.playbooks.models import Playbook


class PlaybookForm(forms.ModelForm):
    name = forms.CharField(
        label="Playbook Name ",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Example: My Playbook",
            "x-model": "playbookName"
        }),
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Example: Steps to onboard a new employee"
        }),
        required=False
    )

    content = forms.CharField(
        label="YAML Content",
        widget=forms.Textarea(attrs={
            "id": "yaml-editor",
        }),
        required=False
    )

    is_public = forms.BooleanField(
        required=False,
        initial=True
    )

    visible_to = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Playbook
        fields = ["name", "description", "content", "is_public", "visible_to", "tags"]