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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.is_bound:
            is_public_now = self.data.get("is_public")
            is_public_now = str(is_public_now).lower() in ("1", "true", "on", "yes")
        else:
            is_public_now = bool(
                self.initial.get("is_public",
                                 getattr(self.instance, "is_public", False))
            )

        self.fields["visible_to"].required = not is_public_now
        if not is_public_now:
            self.fields["visible_to"].required = False
        else:
            self.fields["visible_to"].widget.attrs.pop("required", None)

    def clean(self):
        cleaned_data = super().clean()
        is_public = cleaned_data.get("is_public")
        visible_to = cleaned_data.get("visible_to")

        if not is_public and (not visible_to or visible_to.count() == 0):
            self.add_error(
                "visible_to",
                "This field is required when the playbook is not public. Please select at least one group."
            )

        return cleaned_data
