import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from .chatconsumer import ChatConsumer
from .models import Message, VideoThread, contact

User = get_user_model()


@login_required(login_url='/login')
def chatpage(request):
    recipient = contact.objects.filter()[:1].get()
    user_contact = User.objects.filter(username=recipient).first()

    return redirect('/chat/' + str(user_contact.uuid) + '/')


@login_required(login_url='/login')
def chatroom(request, reciver_uuid):
    print("reciver uuid", reciver_uuid)
    # context =
    return render(request, 'chat/chatroom.html', {'recipient_uuid': mark_safe(json.dumps(reciver_uuid))})


@login_required(login_url='/login')
def video_chat(request, reciver_uuid):
    current_user = request.user
    call_logs = VideoThread.objects.filter(Q(caller_id=current_user.id) | Q(
        callee_id=current_user.id)).order_by('-date_created')[:5]
    return render(request, 'chat/chatroom.html', {'call_logs': call_logs, 'reciver_uuid': reciver_uuid})


@login_required(login_url='/login')
def targeted_recipient(request, reciver_uuid):

    if reciver_uuid:
        recipient = User.objects.get(uuid=reciver_uuid)
        msg_set = Message.objects.filter((Q(sender=request.user) & Q(recipient=recipient)) | (
            Q(sender=request.user) & Q(recipient=recipient))).order_by('-timestamp').all()

        status = 'online'
        # if chname is None:
        #     status = "offline"
        # else:
        #     status = "online"
        #     ChatConsumer.send_chat_msg(
        #         msg=ChatConsumer.user.id, type="status.ON", reciever=recipient)

        ctx = {
            'recipient_uuid': str(recipient.uuid),
            'contact': recipient.id,
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
        'reciver_uuid': mark_safe(reciver_uuid),
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
