from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users.serializers import UserSerializer, AuthTokenSerializer

from django.http import HttpResponse
import sqlite3
import json
import copy
import os
from django.views.generic import TemplateView, View
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from core import models
from . import serializers
from .serializers import UserSignupSerializer, UserSerializerLogin, UserSerializerCreate, UserSerializer, ProfileSerializer, ProfileSerializerUpdate
from core.models import User, Profile
from rest_framework.authtoken.models import Token

class HomePageView(TemplateView):
    template_name = 'home.html'

# profiles
class ProfileView(APIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    @staticmethod
    def get(request):
        """
        List profiles
        """

        profiles = Profile.objects.all()
        return Response(ProfileSerializer(profiles, many=True).data)


# profiles/{profile_id}
class ProfileDetail(APIView):

    @staticmethod
    def patch(request, profile_id):
        """
        Update profile of authenticated user
        """

        profile = get_object_or_404(Profile, pk=profile_id)
        if profile.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = ProfileSerializerUpdate(profile, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(UserSerializerLogin(profile.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#class UserListView(generics.ListCreateAPIView):
class UserListView(APIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


    @staticmethod
    def get(request):
        """
        List users
        """

        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

    @staticmethod
    def post(request):
        """
        Create user
        """

        serializer = UserSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            Profile(user=user).save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class UserDetail(APIView):
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    @staticmethod
    #def get(request, user_id):
    def get(request, pk):

        """
        View individual user
        """

        #user = get_object_or_404(CustomUser, pk=user_id)
        user = get_object_or_404(CustomUser, pk=pk)
        return Response(UserSerializer(user).data)

    @staticmethod
    def patch(request, pk):
    #def put(request, pk):
        """
        Update authenticated user
        """

        user = get_object_or_404(CustomUser, pk=pk)
        if user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializerUpdate(user, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializerLogin(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, user_id):
        """
        Delete user
        """

        user = get_object_or_404(CustomUser, pk=user_id)
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

        
class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSignupSerializer

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

class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializerLogin

    @staticmethod
    def post(request):
        """
        Get user data and API token
        """


        user = get_object_or_404(CustomUser, username=request.data.get('username'))
        user = authenticate(username=user.username, password=request.data.get('password'))
        if user:
            serializer = UserSerializerLogin(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
 

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user
