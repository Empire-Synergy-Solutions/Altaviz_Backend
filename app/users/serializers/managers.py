from rest_framework import serializers
from core.serializers.user import UserSerializer
from users.models.managers import Managers
from utils import constants
from utils.permissions import is_administrator, is_managers


class ManagerSerializer(serializers.ModelSerializer):
    vendors = UserSerializer()
    user = UserSerializer()

    class Meta:
        model = Managers
        fields = '__all__'


class ManagerSerializerCreate(serializers.ModelSerializer):
    vendors = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Managers
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

        if is_managers(user):
            raise serializers.ValidationError('User already has a managers permissions')
        return user
