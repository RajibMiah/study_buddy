from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Room

User = get_user_model()


class StudyBuddyLoginForm(AuthenticationForm):
    """Username / password login with Study Buddy field styling hooks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Username", "autofocus": True}
        )
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})


class UserRegisterForm(UserCreationForm):
    """Account creation form that hashes the password via UserCreationForm."""

    class Meta:
        model = User
        fields = ["name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                "placeholder", field.label or field.name
            )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email exists.")
        return email

    def clean_username(self):
        return self.cleaned_data["username"].lower()


class UserForm(forms.ModelForm):
    """Profile self-service edit form."""

    github = forms.URLField(assume_scheme="https", required=False)
    linkedin = forms.URLField(assume_scheme="https", required=False)
    location = forms.URLField(
        assume_scheme="https", required=False, label="Website"
    )

    class Meta:
        model = User
        fields = [
            "name",
            "username",
            "email",
            "bio",
            "designation",
            "avator",
            "github",
            "linkedin",
            "location",
        ]

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").lower()
        if (
            email
            and User.objects.filter(email__iexact=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("That email is already in use.")
        return email


class RoomForm(forms.ModelForm):
    """Validates room input. The free-text ``topic_name`` is turned into a
    :class:`~base.models.Topic` row by :mod:`base.services`, not here."""

    topic_name = forms.CharField(max_length=255, label="Topic")

    class Meta:
        model = Room
        fields = ["name", "description", "room_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.topic_id:
            self.fields["topic_name"].initial = self.instance.topic.name

    def clean_topic_name(self):
        name = self.cleaned_data["topic_name"].strip()
        if not name:
            raise forms.ValidationError("A topic is required.")
        return name
