from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import Account
from authentication.serializers import CustomUserSerializer


# class CustomUserCreate(APIView):
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 json = serializer.data
#                 return Response(json, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CustomUserCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Account.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlackListTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data['request_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class LoginAPIView(generics.GenericAPIView):
#     permission_classes = (AllowAny,)
#     # renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         user = request.data.get('account', {})
#
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)