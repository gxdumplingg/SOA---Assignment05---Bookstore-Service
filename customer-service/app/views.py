import os

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Address, Customer
from .serializers import AddressSerializer, CustomerSerializer

CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://localhost:8002")


class CustomerViewSet(APIView):
	def get_object(self, pk):
		try:
			return Customer.objects.get(pk=pk)
		except Customer.DoesNotExist:
			return None

	def get(self, request, pk=None):
		if pk is None:
			customers = Customer.objects.all().order_by("id")
			serializer = CustomerSerializer(customers, many=True)
			return Response(serializer.data)

		customer = self.get_object(pk)
		if customer is None:
			return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CustomerSerializer(customer)
		return Response(serializer.data)

	def post(self, request):
		serializer = CustomerSerializer(data=request.data)
		if serializer.is_valid():
			customer = serializer.save()
			try:
				requests.post(
					f"{CART_SERVICE_URL}/api/carts/",
					json={"customer_id": customer.id},
					timeout=5,
				)
			except requests.RequestException:
				pass
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk):
		customer = self.get_object(pk)
		if customer is None:
			return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CustomerSerializer(customer, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk):
		customer = self.get_object(pk)
		if customer is None:
			return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CustomerSerializer(customer, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		customer = self.get_object(pk)
		if customer is None:
			return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

		customer.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class AddressViewSet(APIView):
	def get_object(self, pk):
		try:
			return Address.objects.get(pk=pk)
		except Address.DoesNotExist:
			return None

	def get(self, request, pk=None):
		if pk is None:
			addresses = Address.objects.all().order_by("id")
			serializer = AddressSerializer(addresses, many=True)
			return Response(serializer.data)

		address = self.get_object(pk)
		if address is None:
			return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = AddressSerializer(address)
		return Response(serializer.data)

	def post(self, request):
		serializer = AddressSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk):
		address = self.get_object(pk)
		if address is None:
			return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = AddressSerializer(address, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk):
		address = self.get_object(pk)
		if address is None:
			return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = AddressSerializer(address, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		address = self.get_object(pk)
		if address is None:
			return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

		address.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
