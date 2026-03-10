from rest_framework import serializers

from .models import Address, Customer, FullName


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "customer",
            "line1",
            "line2",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
        ]


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "line1",
            "line2",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
        ]


class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = ["id", "full_name"]
        read_only_fields = ["id"]


class CustomerSerializer(serializers.ModelSerializer):
    fullname = FullNameSerializer(required=False)
    address = AddressCreateSerializer(write_only=True, required=False)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "name", "email", "fullname", "address", "addresses"]

    def create(self, validated_data):
        fullname_data = validated_data.pop("fullname", None)
        address_data = validated_data.pop("address", None)
        customer = Customer.objects.create(**validated_data)

        if fullname_data and fullname_data.get("full_name"):
            FullName.objects.create(customer=customer, full_name=fullname_data["full_name"])

        if address_data and address_data.get("line1"):
            if "is_default" not in address_data:
                address_data["is_default"] = True
            Address.objects.create(customer=customer, **address_data)

        return customer

    def update(self, instance, validated_data):
        fullname_data = validated_data.pop("fullname", None)
        validated_data.pop("address", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if fullname_data and fullname_data.get("full_name"):
            FullName.objects.update_or_create(
                customer=instance,
                defaults={"full_name": fullname_data["full_name"]},
            )

        return instance

