from rest_framework import serializers
from .models import *
from authapp.models import *
from authapp.models import ServiceProvider



"""complete by tasim"""


class ServiceCatSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'category_name', ]


class ServiceSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSubCategory
        fields = ['id', 'category', 'service_sub_category_name',
                  'service_sub_category_keyword']


class ServiceSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_user', 'service_category', 'service_sub_category', 'service_keyword_list', 'service_name', 'service_description',
                  'service_experiance_year',  'rate_apt_video_cons', 'rate_inst_video_cons', 'rate_inhouse_cons', 'rate_promotion',
                  'service_created_date', 'service_status', 'service_visibility', 'service_zip_code']


class ServiceReceivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReceived
        fields = ('__all__')


class addViolationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationType
        fields = ('__all__')


class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = ('__all__')


class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarningModel
        fields = ('__all__')


"""complete by Naznin"""


class ProviderAvailableSerialiser(serializers.Serializer):

    saturday = serializers.BooleanField(default=False)
    sunday = serializers.BooleanField(default=False)
    monday = serializers.BooleanField(default=False)
    tuesday = serializers.BooleanField(default=False)
    wednesday = serializers.BooleanField(default=False)
    thursday = serializers.BooleanField(default=False)
    friday = serializers.BooleanField(default=False)
    all = serializers.BooleanField(default=False)
    # day_name = serializers.CharField(max_length=255)
    appointment_start_date = serializers.DateField()
    appointment_end_date = serializers.DateField()
    day_start_time = serializers.TimeField()
    day_end_time = serializers.TimeField()
    duration = serializers.IntegerField()


class DurationWiseAppointmentInfoSerialiser(serializers.Serializer):

    appointment_start_date = serializers.DateField()
    appointment_end_date = serializers.DateField()


class AppointmentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class CustomerBookAppointmentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_type', 'status', 'appointment_customer']


class CancelAppointmentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['canceled_by', ]




class videoCallingSerializer(serializers.ModelSerializer):
    class Meta:
        model = videoCallingBearerTokenStore
        fields = ('__all__')







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



class ServiceFileSerializer(serializers.ModelSerializer):
    service_image = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = ServiceFile
        fields = ('__all__')

 



class search_service_file_serializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFile
        fields = ['id', 'service_image']



class search_serviceSerialiser(serializers.ModelSerializer):
    service_files = search_service_file_serializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields =  ['id', 'service_user', 'service_category', 'service_sub_category', 'service_keyword_list', 'service_name', 'service_description',
                  'service_experiance_year','service_created_date', 'service_status', 'service_visibility', 'service_zip_code', 'service_files']
        



