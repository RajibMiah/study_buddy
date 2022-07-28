from chat.serializers import MessageModelSerializer, MessageSerializer
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView

User = get_user_model()


class MessageView(CreateAPIView):
    serializer_class = MessageSerializer

    # def post(self, request, *args, **kwargs):
    #     user = User.objects.get(name=1)
    #     print(user.sender)
    #     print('sender id', user.pk)
    #     return self.create(request, *args, **kwargs)
