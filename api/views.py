from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets


from api.serializer import UserSerializer
from core.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'head', 'options']
