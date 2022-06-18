import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.query_utils import Q
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from .chatconsumer import ChatConsumer
from .forms import RegistrationForm
from .models import Message, contact

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

    if reciver_uuid:
        recipient = User.objects.get(uuid=reciver_uuid)
        msg_set = Message.objects.filter((Q(sender=request.user) & Q(recipient=recipient)) | (
            Q(sender=request.user) & Q(recipient=recipient))).order_by('-timestamp').all()
        # chname = contact.objects.get(contact_id_id=recipient.id)

        status = 'online'
        # if chname is None:
        #     status = "offline"
        # else:
        #     status = "online"
        #     # ChatConsumer.send_chat_msg(
        #     #     self=None, msg=request.user.id, type="status.ON", reciever=recipient)

        ctx = {
            'recipient_uuid': str(recipient.uuid),
            # 'contact': data['user'],
            'name': recipient.username,
            'messages': to_json_msgs(msg_set),
            'status': status,
            'pic': recipient.avator.url
        }
        # print('context', ctx)

    return render(request, 'chat/chatpage.html', {
        'username': mark_safe(json.dumps(request.user.username)),
        'userid': mark_safe(json.dumps(request.user.id)),
        'domain': mark_safe(json.dumps(get_current_site(request).domain)),
        'reciver_uuid': reciver_uuid,
        'loaded_msg_details': mark_safe(json.dumps(ctx))
    })


def to_json_msgs(msgs):
    msg_list = []
    for msg in msgs:
        msg_list.append(to_json_msg(msg))
    return msg_list


def to_json_msg(msg):

    return{
        'sid': msg.sender_id,
        'rid': msg.recipient_id,
        'sender': msg.sender.username,
        'recipient': msg.recipient.username,
        'content': msg.content,
        'time_stamp': str(msg.timestamp).split('.')[0],
        'is_readed': msg.is_readed,
        'pic': msg.sender.avator.url
    }
