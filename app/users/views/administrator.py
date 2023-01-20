from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models.administrator import Administrator
from users.models.moderator import Moderator
from users.serializers.administrator import AdministratorSerializer, AdministratorSerializerCreate


# administrators
class AdministratorView(APIView):

    @staticmethod
    def get(request):
        """
        List administrators
        """

        administrators = Administrator.objects.all()
        return Response(AdministratorSerializer(administrators, many=True).data)

    @staticmethod
    def post(request):
        """
        Create administrator
        Remove user as moderator if appointed
        """

        serializer = AdministratorSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            administrator = serializer.save()
            Moderator.objects.filter(user=administrator.user).delete()
            return Response(AdministratorSerializer(administrator).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
