"""
URL configuration for Sleepify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

# Importing the Group model from Django's auth system for custom admin functionalities
# from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Group

# Setting the title displayed on the admin index page
admin.site.index_title = "Business Account"

# Unregistering the default Group model from the admin site to customize admin access and permissions
# admin.site.unregister(User)
admin.site.unregister(Group)

# Including URLs from various apps in the project
urlpatterns = [
    path('business/', admin.site.urls),

    # Custom URLs
    path("user/", include("userauths.urls")),
    path("", include("hotel.urls")),
    path("booking/", include("booking.urls")),
    path("dashboard/", include("user_dashboard.urls")),

    # Including URLs for the CKEditor 5 rich text editor
    path("ckeditor5/", include("django_ckeditor_5.urls"))
]

# Serving static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serving media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
