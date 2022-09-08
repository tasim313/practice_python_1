from unittest import result
from urllib import request
from django.db.models import fields
from django.db import models
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from api.serializers import ServiceSerialiser, ServiceReceivedSerializer
from api.models import Service

User = get_user_model()


class CustomSerializer(serializers.HyperlinkedModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(
            declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class CustomUserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'middle_name', 'last_name', 'email',
                  'phone_number', 'gender', 'joining_date', 'role', 'online_status', 'activity_status',
                  'account_status', 'payment_to_method', 'payment_from_method']


# class ProfilePictureSerialiser(serializers.ModelSerializer):

#     def create(self, validated_data):
#         return ProfilePicture(**validated_data)

#     class Meta:
#         model = ProfilePicture
#         fields = '__all__'


# class UploadVideoModelSerialiser(serializers.ModelSerializer):
#     class Meta:
#         model = UploadVideoModel
#         fields = ['id', 'video_link']


class UserStatusSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'online_status', 'account_status']


class PatchUserStatusSerialiser(serializers.ModelSerializer):

    # provider_service = ServiceSerialiser(many=True)

    class Meta:
        model = User
        fields = ['id', 'online_status', 'account_status', 'activity_status']


# class PatchCustomerStatusSerialiser(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['id','online_status','account_status', 'activity_status']

class CustomerSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class ServiceProviderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'


class AddressSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class AddressTypeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = AddressType
        fields = ['id', 'address_type']


class MyAddressSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street_address',
                  'zip_code', 'state', 'city', 'country']


class UserListSerialiser(serializers.ModelSerializer):

    user_address = MyAddressSerialiser(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'online_status', 'activity_status',
                  'account_status', 'payment_to_method', 'payment_from_method', 'user_address')


class SearchServicesProviderSerialiser(serializers.ModelSerializer):
    user_address = MyAddressSerialiser(read_only=True, many=True)
    user_service_provider = ServiceProviderSerialiser(read_only=True)
    service_of_user = ServiceSerialiser(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'online_status', 'activity_status',
                  'account_status', 'payment_to_method', 'payment_from_method',
                  'user_address', 'user_service_provider', 'service_of_user')


class pref_provider_Customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PreProvider
        fields = ('id', 'user_customer', 'provider', 'customer_name', 'provider_name')


class customer_list_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class provider_customer_list_Serializer(serializers.ModelSerializer):
    user_info = customer_list_Serializer(read_only=True, many=True)
    user_address = MyAddressSerialiser(read_only=True, many=True)

    class Meta:
        model = Customer
        fields = ('id', 'user_customer', 'user_info', 'user_address')




# class UploadProfilePictureSerializer(serializers.ModelSerializer):
#     profile_picture = serializers.ImageField(max_length=None, use_url=True)

#     class Meta:
#         model = ProfilePicture
#         fields = ('__all__')



class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            # 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class UploadProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = ProfilePicture
        fields = ('__all__')



class AddressZipCodeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['zip_code']
