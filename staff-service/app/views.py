from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Staff
from .serializers import StaffSerializer


class StaffViewSet(APIView):
    def get_object(self, pk):
        try:
            return Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk is None:
            staff_qs = Staff.objects.all().order_by("id")
            serializer = StaffSerializer(staff_qs, many=True)
            return Response(serializer.data)

        staff = self.get_object(pk)
        if staff is None:
            return Response({"detail": "Staff not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(staff)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        staff = self.get_object(pk)
        if staff is None:
            return Response({"detail": "Staff not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        staff = self.get_object(pk)
        if staff is None:
            return Response({"detail": "Staff not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(staff, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        staff = self.get_object(pk)
        if staff is None:
            return Response({"detail": "Staff not found."}, status=status.HTTP_404_NOT_FOUND)

        staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
