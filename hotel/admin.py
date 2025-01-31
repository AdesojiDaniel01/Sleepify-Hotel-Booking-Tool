from django.contrib import admin
from hotel.models import Hotel, Room, HotelGallery, HotelFeatures, RoomType
from import_export.admin import ImportExportModelAdmin


# Inline class to allow adding/editing HotelGallery objects within the HotelAdmin form
class HotelGalleryInline(admin.TabularInline):
    model = HotelGallery


# Inline class to allow adding/editing HotelFeatures objects within the HotelAdmin form
class HotelFeaturesInline(admin.TabularInline):
    model = HotelFeatures


# Inline class to allow adding/editing Room objects within the HotelAdmin form
class RoomInline(admin.TabularInline):
    model = Room


# Inline class to allow adding/editing RoomType objects within the HotelAdmin form
class RoomTypeInline(admin.TabularInline):
    model = RoomType


# Admin class for managing Hotel objects with additional functionalities
class HotelAdmin(ImportExportModelAdmin):
    # Allows inline editing of related models (Gallery, Features, Rooms, RoomTypes) in the Hotel admin form
    inlines = [HotelGalleryInline, HotelFeaturesInline,
               RoomTypeInline, RoomInline]

    search_fields = ['user__username', 'name']
    list_filter = ['status']
    list_editable = ['status']
    # list_display = ['thumbnail', 'user',
    #                 'name', 'status']
    list_display = ['thumbnail', 'name', 'status']

    # Limits the number of entries shown per page in the list view
    list_per_page = 100

    # Automatically generates the 'slug' field from the 'name' field when creating a hotel
    prepopulated_fields = {"slug": ("name", )}


# Admin class for managing Room objects
class RoomAdmin(ImportExportModelAdmin):
    list_display = ['hotel', 'room_number',  'room_type',
                    'price', 'number_of_beds', 'is_available']
    list_per_page = 100


# It includes list filters, search fields, and display options for booking information
# class BookingAdmin(ImportExportModelAdmin):
#     list_filter = ['hotel', 'room_type', 'check_in_date',
#                    'check_out_date', 'is_active', 'checked_in', 'checked_out']
#     list_display = ['booking_id', 'user', 'hotel', 'room_type', 'rooms', 'total', 'total_days', 'num_adults',
#                     'num_children', 'check_in_date', 'check_out_date', 'is_active', 'checked_in', 'checked_out']
#     search_fields = ['booking_id', 'user__username', 'user__email']
#     list_per_page = 100


# Registers the models in the hotel admin / property owner view
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType)
# admin.site.register(Booking, BookingAdmin)
