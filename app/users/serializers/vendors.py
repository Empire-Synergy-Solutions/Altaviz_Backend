from rest_framework import serializers
from core.serializers.user import UserSerializer
from users.models.vendors import Vendors
from utils import constants
from utils.permissions import is_administrator, is_vendors


class ModeratorSerializer(serializers.ModelSerializer):
    #sponsor = UserSerializer()
    user = UserSerializer()

    class Meta:
        model = Vendors
        fields = '__all__'


class ModeratorSerializerCreate(serializers.ModelSerializer):
    #sponsor = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vendors
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

        if is_vendors(user):
            raise serializers.ValidationError('User already has vendors permissions')
        return user
