from django.core.validators import RegexValidator
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from authentication.models import Account


class CustomUserSerializer(serializers.ModelSerializer):
    unique_validator = UniqueValidator(queryset=Account.objects.all())
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,12}$',
        message="Phone number must be entered in the format: '+84123456789'. Up to 12 digits allowed."
    )
    email = serializers.EmailField(required=True, validators=[unique_validator])
    username = serializers.CharField(required=True, max_length=50, validators=[unique_validator])
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False, max_length=50)
    last_name = serializers.CharField(required=False, max_length=50)
    phone = serializers.CharField(required=False, max_length=12, validators=[phone_regex])
    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = Account
        fields = (
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'phone',
            'is_staff',
            'is_superuser',
            'is_active',
        )

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # def update(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=50, required=True)
#     password = serializers.CharField(required=True)
#
#     def validate(self, attrs):
#         username = attrs.get('username', None)
#         password = attrs.get('password', None)
#
#         if username is None:
#             raise serializers.ValidationError('Require username')
#         if password is None:
#             raise serializers.ValidationError('Require password')
#
#         user = authenticate(username=username, password=password)
#         if user is None:
#             raise serializers.ValidationError('Wrong username or password')
#         if not user.is_active:
#             raise serializers.ValidationError('This user has been deactivated')
#
#         return {
#             'username': user.username,
#             'token': user.token
#         }
