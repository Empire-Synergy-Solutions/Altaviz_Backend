from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import Profile, User
#from core.models.user import User
from utils import constants
from utils.permissions import is_administrator, is_moderator, is_customers, is_vendors, is_attendants, is_managers
from .profile import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name',
                  'last_name', 'profile', 'role')

    @staticmethod
    def get_profile(user):
        """
        Get or create profile
        """

        profile, created = Profile.objects.get_or_create(user=user)
        return ProfileSerializer(profile, read_only=True).data

    @staticmethod
    def get_role(user):
        """
        Get user role
        """

        if is_administrator(user):
            return constants.USER_ROLE_ADMINISTRATOR
        if is_moderator(user):
            return constants.USER_ROLE_MODERATOR
        if is_customers(user):
            return constants.USER_ROLE_CUSTOMERS
        if is_vendors(user):
            return constants.USER_ROLE_VENDORS
        if is_managers(user):
            return constants.USER_ROLE_MANAGERS
        if is_attendants(user):
            return constants.USER_ROLE_ATTENDANTS
        


class UserSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'phone_number',
                  'first_name', 'last_name', 'password')

    def validate(self, data):
        """
        Administrator permissions needed
        """

        if not is_administrator(self.context['request'].user):
            raise serializers.ValidationError(
                constants.PERMISSION_ADMINISTRATOR_REQUIRED)
        return data

    @staticmethod
    def validate_password(password):
        """
        Validate password
        """

        validate_password(password)
        return password


class UserSerializerLogin(UserSerializer):
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user):
        """
        Get or create token
        """

        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name',
                  'last_name', 'profile', 'role', 'token')


class UserSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
