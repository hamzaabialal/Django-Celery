from django.shortcuts import render
from .serializers import NotificationSerializer, EmailSerializers, CustomUserSerializer, LoginInSerializer
from .models import Notification, Email, CustomUser
from rest_framework.generics import ListCreateAPIView
from .task import send_mail_func
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate

# Create your views here.
class NotificationView(ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.request.data.get('status') == 'unread':
            send_mail_func.delay()
        return response
    
    # def get_queryset(self):
    #     return Notification.objects.filter(status='unread')
    # send_email_fucn.delay()


class EmailView(ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class SignupView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class LoginView(CreateModelMixin, GenericViewSet):
    serializer_class = LoginInSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token= str(refresh)
            return Response({
                'refresh': refresh_token,
                'access': access_token,
                'message': 'Login successfully',
                'status': 200
            })
        return Response({'message': 'Invalid credentials'}, status=401)