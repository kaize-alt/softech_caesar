from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .models import CustomUser
from .serializers import LoginSerializer, ResetPasswordSerializer, UserRegisterSerializer


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

        if password == password_confirm:
            # Save the user instance (create user and handle password setting)
            instance = serializer.save()
            return Response(self.get_serializer(instance).data)  # Return serialized response
        instance = serializer.save()
        return Response(self.get_serializer(instance).data)

        return Response({"error": "Пароли не совпадают"}, status=400)



class LoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)
        email = data.validated_data.get("email")
        password = data.validated_data.get("password")
        user = CustomUser.objects.filter(email=email).first()

        if user:
            if check_password(password, user.password):
                return Response({"message": "Добро пожаловать"}, status=HTTP_200_OK)
            return Response({"error":  "Вы ввели не правильный пароль"}, status=HTTP_400_BAD_REQUEST)
        return Response({"error": "Пользователь с такой почтой не найден"}, status=HTTP_404_NOT_FOUND)


class ResetPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user_email = CustomUser.objects.filter(email=email).first()
        if user_email:
            connection = smtp()
            message_text = "Для сброса и обновления пароля перейдите по ссылке: "
            message = EmailMessage(
                subject="Письмо для сброса и обновления пароля",
                body=message_text,
                from_email="omurkanovd22@gmail.com",
                to=[email]
            )
            connection.send_messages([message])
            return Response(self.get_serializer(serializer.instance).data)
        return Response({"error": "Пользователь с такой почтой не найдет"}, status=HTTP_404_NOT_FOUND)
