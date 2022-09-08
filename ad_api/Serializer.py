from rest_framework import serializers
from . models import *


class AD_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ad
        fields = ('id', 'ad_type', 'rate_per_show', 'rate_per_click', 'start_date', 'end_date', 'show_count',
                  'click_count', 'window_size_list', 'window_location_list', 'ad_tag_list', 'audience_interest_type')


class AdInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdInterest
        fields = '__all__'


class GetADSerializer(serializers.ModelSerializer):
    class Meta:
        model = ad
        fields = ('id', 'ad_type', 'rate_per_show', 'rate_per_click', 'start_date', 'end_date', 'show_count',
                  'click_count', 'window_size_list', 'window_location_list', 'ad_tag_list', 'audience_interest_type')


class UploadImageADMediaSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = UploadADMedia
        exclude = ('video', )


class UploadVideoADMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadADMedia
        exclude = ('image',)


class Link_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class Link_choise_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('link_type', )


class Link_Image_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        exclude = ('link_type', 'video', 'link_url')


class Link_Video_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        exclude = ('link_type', 'image', 'link_url')
