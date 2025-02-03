from rest_framework import serializers

from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, required=True)
    is_read = serializers.BooleanField(default=False, write_only=True)
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "email",
            "phone_number",
            "address",
            "password",
            "password_confirm",
            "is_read"
        )

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        validated_data.pop("is_read", None)

        user = CustomUser(**validated_data)

        password = validated_data.get('password')
        user.set_password(password)

        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password")


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ("email",)
