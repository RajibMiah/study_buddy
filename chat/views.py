import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from .forms import RegistrationForm


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

    # TODO:: find first message in model contact by channel_name which is uuid and pass it to targeted_reciver view

    return render(request, 'chat/chatpage.html', {
        'username': mark_safe(json.dumps(request.user.username)),
        'userid': mark_safe(json.dumps(request.user.id)),
        'domain': mark_safe(json.dumps(get_current_site(request).domain)),
    })


@login_required
def targeted_reciver(request, reciver_uuid):
    print('~~~DEBUG~~~')
    print('reciver uuid', reciver_uuid)
    return render(request, 'chat/chatpage.html', {
        'username': mark_safe(json.dumps(request.user.username)),
        'userid': mark_safe(json.dumps(request.user.id)),
        'domain': mark_safe(json.dumps(get_current_site(request).domain)),
        'reciver_uuid': reciver_uuid
    })
