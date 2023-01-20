from rest_framework import serializers
from core.serializers.user import UserSerializer
from users.models.attendants import Attendants
from utils import constants
from utils.permissions import is_administrator, is_attendants


class AttendantSerializer(serializers.ModelSerializer):
    vendors = UserSerializer()
    user = UserSerializer()

    class Meta:
        model = Attendants
        fields = '__all__'


class AttendantSerializerCreate(serializers.ModelSerializer):
    vendors = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Attendants
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
        Ensure user is not already attendant or higher
        """

        if is_attendants(user):
            raise serializers.ValidationError('User already has attendants permissions')
        return user
