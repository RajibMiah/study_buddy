import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from .forms import RegistrationForm
from .models import contact

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def chatpage(request):
    recipient = contact.objects.filter()[:1].get()
    user_contact = User.objects.filter(username=recipient).first()

    return redirect('/chat/' + str(user_contact.uuid) + '/')


@login_required
def targeted_recipient(request, reciver_uuid):
    return render(request, 'chat/chatpage.html', {
        'username': mark_safe(json.dumps(request.user.username)),
        'userid': mark_safe(json.dumps(request.user.id)),
        'domain': mark_safe(json.dumps(get_current_site(request).domain)),
        'reciver_uuid': reciver_uuid
    })
