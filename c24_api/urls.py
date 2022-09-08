"""c24_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='C24 API')


urlpatterns = [

    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path('auth_api/', include('authapp.urls')),
    path('api/', include('api.urls')),
    path('ad_api/', include('ad_api.urls')),
    path('billing/', include('billing.urls')),
    path('review/', include('Reviews.urls')),
    path('ticket_info/', include('TicketInfo.urls')),
    path('invoice_info/', include('Invoicing.urls')),
    path('videocall/', include('videocalling.urls')),

    path('docs/', schema_view),
    # social media authentication urls
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
