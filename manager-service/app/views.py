from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Manager
from .serializers import ManagerSerializer


class ManagerViewSet(APIView):
    def get_object(self, pk):
        try:
            return Manager.objects.get(pk=pk)
        except Manager.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk is None:
            managers = Manager.objects.all().order_by("id")
            serializer = ManagerSerializer(managers, many=True)
            return Response(serializer.data)

        manager = self.get_object(pk)
        if manager is None:
            return Response({"detail": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ManagerSerializer(manager)
        return Response(serializer.data)

    def post(self, request):
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        manager = self.get_object(pk)
        if manager is None:
            return Response({"detail": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ManagerSerializer(manager, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        manager = self.get_object(pk)
        if manager is None:
            return Response({"detail": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ManagerSerializer(manager, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        manager = self.get_object(pk)
        if manager is None:
            return Response({"detail": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)

        manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
