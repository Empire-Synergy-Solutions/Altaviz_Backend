from rest_framework import serializers
from core import models
from users.models.customers import Customers
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from core.serializers.user import UserSerializer
#from users.models.customers import Customers
from utils import constants
from utils.permissions import is_administrator, is_customers


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = Customers
        fields = ('email', 'password', 'first_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return Customers.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CustomerSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('first_name', 'last_name',
                  'phone_number', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Customers.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class CustomerSerializerLogin(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = ('phone_number', 'password', 'token', 'email', 'is_active',
                  'is_staff', 'date_joined', 'first_name', 'last_name')
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

        user, created = Customers.objects.get_or_create(user=user)
        return UserSerializer(user, read_only=True).data

    @staticmethod
    def get_token(user):
        """
        Get or create token
        """

        token, created = Token.objects.get_or_create(user=user)
        return token.key


class CustomerSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Customers
        fields = ('email', 'first_name', 'last_name',
                  'password', 'phone_number',)


class CustomerSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Customers
        fields = ('first_name', 'last_name', 'email',
                  'is_active', 'is_staff', 'date_joined', )
        extra_kwargs = {'password': {'write_only': True},
                        'date_joined': {'read_only': True}
                        }

class CustomerSerializer(serializers.ModelSerializer):
    #sponsor = UserSerializer()
    user = UserSerializer()

    class Meta:
        model = Customers
        fields = '__all__'


class CustomerSerializerCreate(serializers.ModelSerializer):
    #sponsor = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Customers
        fields = '__all__'

    def validate(self, data):
        """
        Administrator permissions needed
        """

        if not is_administrator(self.context['request'].user):
            raise serializers.ValidationError(constants.PERMISSION_ADMINISTRATOR_REQUIRED)
        return data

    def validate_user(self, user):
        """
        Ensure user is not already moderator or higher
        """

        if is_customers(user):
            raise serializers.ValidationError('User already has customer permissions')
        return user
