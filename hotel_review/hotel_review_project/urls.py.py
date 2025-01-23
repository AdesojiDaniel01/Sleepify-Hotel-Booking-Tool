from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('', include('hotel_reviews.urls')),  # Include the URLs from the 'hotel_reviews' app
]
