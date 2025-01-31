from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
# from taggit.managers import TaggableManager
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
import shortuuid

from django.template.defaultfilters import escape

# Choices for hotel status
HOTEL_STATUS = (
    ("Live", "Live"),
    ("Under Maintanence", "Under Maintenance"),
    ("Closed", "Closed"),
)



# Choices for icon type in hotel features
ICON_TYPE = (
    ("Boostrap Icons", "Boostrap Icons"),
    ("Fontawesome Icons", "Fontawesome Icons"),
)


# Choices for payment status in bookings
PAYMENT_STATUS = (
    ("Paid", "Paid"),
    ("Pending", "Pending"),
    ("Processing", "Processing"),
    ("Canceled", "Canceled"),
    ("Refunded", "Refunded"),
)


# Hotel Model and its attributes
# This model represents the Hotel table in the database,
# defining the structure and fields associated with a hotel,
# including relationships to other models, and fields for
# storing information.
class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = CKEditor5Field(null=True, blank=True, config_name='extends')
    image = models.FileField(upload_to="hotel_gallery")
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    email = models.EmailField(max_length=320)
    status = models.CharField(
        max_length=20, choices=HOTEL_STATUS, default="Live")

    # tags = TaggableManager(blank=True)

    # Unique hotel identifier using ShortUUID
    hid = ShortUUIDField(unique=True, length=10, max_length=20,
                         alphabet="abcdefghijklmnopqrstuvxyz")

    # Slug field for SEO-friendly URLs
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    # Social media fields (optional)
    facebook = models.URLField(max_length=500, null=True, blank=True)
    instagram = models.URLField(max_length=500, null=True, blank=True)
    twitter = models.URLField(max_length=500, null=True, blank=True)
    linkedin = models.URLField(max_length=500, null=True, blank=True)
    youtube = models.URLField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        # String representation of the hotel (name)
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate a slug if not provided
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.type) + "-" + str(uniqueid.lower())

        super(Hotel, self).save(*args, **kwargs)  # Call the parent save method

    def thumbnail(self):
        # Return a safe HTML representation of the hotel image thumbnail
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))

    def hotel_gallery(self):
        # Retrieve all images associated with this hotel
        return HotelGallery.objects.filter(hotel=self)

    def hotel_features(self):
        # Retrieve all features associated with this hotel
        return HotelFeatures.objects.filter(hotel=self)

    def hotel_room_types(self):
        # Retrieve all room types associated with this hotel
        return RoomType.objects.filter(hotel=self)
        # return RoomType.objects.filter(hotel=self).exists()


# Hotel Gallery Model and its attributes
# This model represents the HotelGallery table in the database,
# which stores images associated with a specific hotel.
class HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.FileField(upload_to="hotel_gallery")
    hgid = ShortUUIDField(unique=True, length=10, max_length=20,
                          alphabet="abcdefghijklmnopqrstuvxyz")

    def __str__(self):
        return str(self.hotel.name)

    class Meta:
        verbose_name_plural = "Hotel Gallery"


# Hotel Features Model and its attributes
# This model represents the HotelFeatures table in the database,
# storing various features associated with a hotel.
class HotelFeatures(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    icon_type = models.CharField(
        max_length=100, null=True, blank=True, choices=ICON_TYPE)
    icon = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        # String representation of the hotel (name)
        return str(self.name)

    class Meta:
        verbose_name_plural = "Hotel Features"


# Room Type Model and its attributes
# This model represents the RoomType table in the database,
# defining different types of rooms available in a hotel.
class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, )
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_beds = models.PositiveIntegerField(default=0)
    room_capacity = models.PositiveIntegerField(default=0)
    rtid = ShortUUIDField(unique=True, length=10, max_length=20,
                          alphabet="abcdefghijklmnopqrstuvxyz")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation of the room type
        return f"{self.type} - {self.hotel.name} - {self.price}"

    class Meta:
        verbose_name_plural = "Room Type"

    def rooms_count(self):
        # Count the number of rooms associated with this room type
        Room.objects.filter(room_type=self).count()

    def save(self, *args, **kwargs):
        # Automatically create a slug if it doesn't exist
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.type) + "-" + str(uniqueid.lower())

        # Call the parent class save method
        super(RoomType, self).save(*args, **kwargs)


# Room Model and its attributes
# This model represents the Room table in the database,
# which stores individual room instances within a hotel.
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=1000)
    is_available = models.BooleanField(default=True)
    rid = ShortUUIDField(unique=True, length=10, max_length=20,
                         alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation of the room type
        return f"{self.room_type.type} - {self.hotel.name}"

    class Meta:
        verbose_name_plural = "Rooms"

    def price(self):
        # Return the price of the room based on the associated room type
        return self.room_type.price

    def number_of_beds(self):
        # Return the number of beds in the room based on the associated room type
        return self.room_type.number_of_beds


# Booking Model and its attributes
# This model represents the Booking table in the database,
# capturing all necessary information related to hotel bookings.
class Booking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS)
    full_name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    phone = models.CharField(max_length=1000)

    hotel = models.ForeignKey(
        Hotel, on_delete=models.SET_NULL, null=True, blank=True)

    room_type = models.ForeignKey(
        RoomType, on_delete=models.SET_NULL, null=True, blank=True)

    room = models.ManyToManyField(Room)
    total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    total_days = models.PositiveIntegerField(default=0)
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)

    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    checked_in_tracker = models.BooleanField(default=False)
    checked_out_tracker = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent = models.CharField(
        max_length=1000, null=True, blank=True)
    success_id = ShortUUIDField(length=10, max_length=20,
                                alphabet="abcdefghijklmnopqrstuvxyz", null=True, blank=True)
    booking_id = ShortUUIDField(unique=True, length=10, max_length=20,
                                alphabet="abcdefghijklmnopqrstuvxyz")

    def __str__(self):
        # String representation of the room
        return f"{self.booking_id}"

    def rooms(self):
        # Return the number of rooms of the rooms
        return self.room.all().count()
