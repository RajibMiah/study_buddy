from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Room, Topic

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
    """Room create / edit. ``topic`` is entered as free text and resolved
    to a :class:`~base.models.Topic` row on save."""

    topic_name = forms.CharField(max_length=255, label="Topic")

    class Meta:
        model = Room
        fields = ["name", "description", "room_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.topic_id:
            self.fields["topic_name"].initial = self.instance.topic.name

    def clean_topic_name(self):
        return self.cleaned_data["topic_name"].strip()

    def save(self, commit=True):
        topic, _ = Topic.objects.get_or_create(
            name=self.cleaned_data["topic_name"]
        )
        self.instance.topic = topic
        return super().save(commit=commit)
