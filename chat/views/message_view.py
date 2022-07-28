from chat.serializers import MessageModelSerializer, MessageSerializer
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView


class MessageView(CreateAPIView):
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=1)
        print(user.sender)
        return self.create(request, *args, **kwargs)
