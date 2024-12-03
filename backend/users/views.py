from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserRegisterSerializer


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get("password")
        password_confirm = serializer.validated_data.get("password_confirm")
        is_read = serializer.validated_data.get("is_read")


        if password != password_confirm:
            return Response({"error": "Пароли не совпадают"}, status=400)
        elif is_read is False:
            return Response({"error": "Вы должны прочитать и согласится с Политика конфиденциальности!"}, status=400)

        instance = serializer.save()
        return Response(self.get_serializer(instance).data)
