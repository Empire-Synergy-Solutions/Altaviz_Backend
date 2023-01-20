from django.shortcuts import render, redirect
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

#from users.serializers.customers import UserSerializer, AuthTokenSerializer

from django.http import HttpResponse
import sqlite3
import json
import copy
import os
from django.views.generic import TemplateView, View, CreateView
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from users import serializers
from users.serializers.customers import CustomerSignupSerializer, CustomerSerializerLogin, CustomerSerializerCreate, CustomerSerializer
from users.models.customers import Customers
from core.models import Profile
from rest_framework.authtoken.models import Token
from users.forms.customer import CustomerWaitListForm
from users import models
#from django.views.generic import TemplateView, CreateView

class CustomerListView(APIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = models.customers.Customers.objects.all()
    serializer_class = CustomerSerializer


    @staticmethod
    def get(request):
        """
        List users
        """

        users = Customers.objects.all()
        return Response(CustomerSerializer(users, many=True).data)

    @staticmethod
    def post(request):
        """
        Create user
        """

        serializer = CustomerSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            Profile(user=user).save()
            return Response(CustomerSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class UserDetail(APIView):
class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

    @staticmethod
    #def get(request, user_id):
    def get(request, pk):

        """
        View individual user
        """

        #user = get_object_or_404(CustomUser, pk=user_id)
        user = get_object_or_404(Customers, pk=pk)
        return Response(CustomerSerializer(user).data)

    @staticmethod
    def patch(request, pk):
    #def put(request, pk):
        """
        Update authenticated user
        """

        user = get_object_or_404(Customers, pk=pk)
        if user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CustomerSerializerUpdate(user, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomerSerializerLogin(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, user_id):
        """
        Delete user
        """

        user = get_object_or_404(Customers, pk=user_id)
        if is_administrator(user) or user.is_superuser:
            return Response({
                constants.ERROR: 'That user can not be deleted'
            }, status=status.HTTP_401_UNAUTHORIZED)
        if is_moderator(user) and not is_administrator(request.user):
            return Response({
                constants.ERROR: 'Admin permissions needed to delete moderators'
            }, status=status.HTTP_401_UNAUTHORIZED)
        if not is_moderator(request.user):
            return Response({
                constants.ERROR: 'Moderator permissions needed to delete users'
            }, status=status.HTTP_401_UNAUTHORIZED)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
class CustomerCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CustomerSignupSerializer

    @staticmethod
    def post(request):
        """
        create user
        """

        serializer = UserSignupSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializerLogin(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerWaitListView(CreateView):
    model = Customers
    form_class = CustomerWaitListForm
    template_name = 'account/signup_form.html'

    def get_context_data(self,*args,**kwargs):
        kwargs['user_type'] = 'Everyday User'
        return super().get_context_data(*args,**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')