from django.db import models
from authapp.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Link(models.Model):
    VIDEO_TYPE = 'VIDEO_TYPE'
    IMAGE_TYPE = 'IMAGE_TYPE'
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_link_id')
    link_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Link Name')
    description = models.TextField(
        verbose_name='Description', blank=True, null=True)
    link_type_choise = [('VIDEO_TYPE', 'Video_Link'),
                        ('IMAGE_TYPE', 'Image_Link')]
    link_type = models.CharField(
        max_length=10, choices=link_type_choise, verbose_name='Link Type', blank=True, null=True)
    link_url = models.URLField(verbose_name='Link URL', blank=True, null=True)

    def __str__(self):
        return f'{self.link_name} ||{self.link_type} ||{self.link_url}'


class ad(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_ad_id')
    link_id = models.ForeignKey(
        Link, on_delete=models.CASCADE, related_name='link_ad_id', blank=True, null=True)

    ad_type_choices = [
        ('VIDEO', 'Video'),
        ("IMAGE", 'Image')
    ]

    ad_type = models.CharField(max_length=10, choices=ad_type_choices)
    rate_per_show = models.CharField(max_length=255, blank=True, null=True)
    rate_per_click = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    show_count = models.IntegerField()
    click_count = models.IntegerField()
    window_size_list = ArrayField(models.PositiveIntegerField(
        null=True, blank=True), null=True, blank=True, default=[])
    window_location_list = ArrayField(models.TextField(
        null=True, blank=True), null=True, blank=True, default=[])

    ad_tag_list = ArrayField(models.TextField(
        null=True, blank=True), null=True, blank=True, default=[])

    audience_interest_type_choise = [
        ('CUSTOMER', 'Customer'),
        ('PROVIDER', 'Provider'),
        ('ALL_USER', 'All_User')
    ]
    audience_interest_type = models.CharField(
        max_length=25, choices=audience_interest_type_choise)

    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.ad_type}|| {self.start_date} || {self.end_date}'


class UserAdInterest(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_adinterest_id')
    ad_tag_list = ArrayField(models.TextField(
        null=True, blank=True), null=True, blank=True, default=[])

    entry_date = models.DateTimeField(auto_now_add=True)


class UploadADMedia(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_uploadadmedia')
    image = models.ImageField(upload_to='AD_Image', blank=True, null=True)
    video = models.FileField(upload_to='AD_Video', blank=True, null=True)
