from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework import serializers
from core import models
from core.models import User, Profile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
#from .serializers import UserSerializer

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #profile = serializers.SerializerMethodField()
        model = models.User
        fields = ('email', 'phone_number', 'first_name', 'last_name','is_active', 'is_staff', )

    @staticmethod
    def get_profile(user):
        """
        Get or create profile
        """
        user, created = CustomUser.objects.get_or_create(user=user)
        #profile, created = Profile.objects.get_or_create(user=user)
        #return ProfileSerializer(profile, read_only=True).data
        return UserSerializer(user, read_only=True).data



class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ( 'first_name', 'last_name', 'phone_number', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class UserSerializerLogin(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ( 'phone_number', 'password','token', 'email', 'is_active', 'is_staff', 'date_joined', 'first_name', 'last_name' )
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'read_only': True},
                        'is_active': {'read_only': True},
                        'is_staff': {'read_only': True},
                        'date_joined': {'read_only': True},
                        'first_name': {'read_only': True},
                        'last_name': {'read_only': True}
                         }

    @staticmethod
    def get_profile(user):
        """
        Get or create profile
        """

        user, created = CustomUser.objects.get_or_create(user=user)
        return UserSerializer(user, read_only=True).data    


    @staticmethod
    def get_token(user):
        """
        Get or create token
        """

        token, created = Token.objects.get_or_create(user=user)
        return token.key


class UserSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password','phone_number',)


class UserSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'is_active', 'is_staff', 'date_joined', )
        extra_kwargs = {'password': {'write_only': True},
                        'date_joined': {'read_only': True}
                        }



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'

    @staticmethod
    def get_profile(user):
        """
        Get or create profile
        """
        #user, created = CustomUser.objects.get_or_create(user=user)
        profile, created = Profile.objects.get_or_create(user=user)
        return ProfileSerializer(profile, read_only=True).data


class ProfileSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('image',)