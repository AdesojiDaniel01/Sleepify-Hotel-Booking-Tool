from django.shortcuts import render, redirect
from hotel.models import Hotel, Room, Booking, HotelGallery, HotelFeatures, RoomType
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django. urls import reverse
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from datetime import datetime
import stripe
from decimal import Decimal


# View to display the list of live hotels
# This view retrieves all hotels that are currently marked as "Live"
# in the database. It fetches these hotels from the Hotel model
# and passes them to the hotel list template for rendering.
# The retrieved hotels are displayed to users on the homepage
# or any designated landing page for hotel browsing.
def index(request):
    hotels = Hotel.objects.filter(status="Live")
    context = {
        "hotels": hotels
    }
    return render(request, "hotel/hotel.html", context)


# View to display the details of a specific hotel
# This view retrieves the details of a specific hotel based on the
# provided slug. It ensures that only hotels marked as "Live" are
# accessible, enhancing the user experience by preventing
# access to unavailable hotels. The hotel details are passed to
# the hotel detail template for rendering, allowing customers to view
# more information about the selected hotel.
def hotel_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context = {
        "hotel": hotel,

    }

    return render(request, "hotel/hotel_detail.html", context)


# View to display the details of a specific room type in a hotel
# This view retrieves the details of a room type within a specific
# hotel based on the provided slugs. It ensures that the hotel
# is marked as "Live" and fetches available rooms of the selected
# room type. Additionally, it collects query parameters for check-in,
# check-out dates, and the number of adults and children, which
# will be displayed to users, enhancing the booking experience
# by providing all necessary information in one place.
def room_type_detail(request, slug, rt_slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    room_type = RoomType.objects.get(hotel=hotel, slug=rt_slug)
    rooms = Room.objects.filter(room_type=room_type, is_available=True)

    id = request.GET.get("hotel-id")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")
    adult = request.GET.get("adult")
    children = request.GET.get("children")

    context = {
        "hotel": hotel,
        "room_type": room_type,
        "rooms": rooms,
        "checkin": checkin,
        "checkout": checkout,
        "adult": adult,
        "children": children,
    }

    return render(request, "hotel/room_type_detail.html", context)


# View to handle selected room bookings and calculate total costs
# This view manages the booking process by retrieving data from
# the user's session, including selected hotels, check-in and
# check-out dates, and the number of guests. It calculates
# the total cost based on the selected rooms and the length of
# stay, and it creates a new Booking object with the provided
# user information. The view also handles redirection to the
# checkout process once the booking is created, ensuring a
# smooth user experience.
def selected_rooms(request):
    total = 0
    room_count = 0
    total_days = 0
    adult = 0
    children = 0
    checkin = ""
    checkout = ""

    if 'selection_data_obj' in request.session:

        if request.method == "POST":
            for h_id, item in request.session['selection_data_obj'].items():
                # print(h_id, item)
                id = int(item['hotel_id'])

                checkin = item['checkin']
                checkout = item['checkout']
                adult = int(item['adult'])
                children = int(item['children'])
                room_type_ = int(item['room_type'])
                room_id = int(item['room_id'])

                user = request.user
                hotel = Hotel.objects.get(id=id)
                room = Room.objects.get(id=room_id)
                room_type = RoomType.objects.get(id=room_type_)

            date_format = "%Y-%m-%d"
            checkin_date = datetime.strptime(checkin, date_format)
            checkout_date = datetime.strptime(checkout, date_format)
            time_difference = checkout_date - checkin_date
            total_days = time_difference.days

            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            booking = Booking.objects.create(
                hotel=hotel,
                room_type=room_type,
                check_in_date=checkin,
                check_out_date=checkout,
                total_days=total_days,
                num_adults=adult,
                num_children=children,
                full_name=full_name,
                email=email,
                phone=phone,
                user=request.user or None,
                payment_status="Processing",
            )

            # if request.user.is_authenticated:
            #     booking.user = request.user
            #     booking.save()
            # else:
            #     booking.user = None
            #     booking.save()

            for h_id, item in request.session['selection_data_obj'].items():
                room_id = int(item["room_id"])
                room = Room.objects.get(id=room_id)
                booking.room.add(room)

                room_count += 1
                days = total_days
                price = room_type.price

                room_price = price * room_count
                total = room_price * days

            booking.total += float(total)
            booking.save()

            # messages.success(request, "Checkout Now")
            return redirect("hotel:checkout", booking.booking_id)

        hotel = None
        for h_id, item in request.session['selection_data_obj'].items():
            # print(h_id, item)
            id = int(item['hotel_id'])
            checkin = item['checkin']
            checkout = item['checkout']
            adult = int(item['adult'])
            children = int(item['children'])
            room_type_ = int(item['room_type'])
            room_id = int(item['room_id'])

            room_type = RoomType.objects.get(id=room_type_)

            date_format = "%Y-%m-%d"
            checkin_date = datetime.strptime(checkin, date_format)
            checkout_date = datetime.strptime(checkout, date_format)
            time_difference = checkout_date - checkin_date
            total_days = time_difference.days

            room_count += 1
            days = total_days
            price = room_type.price

            room_price = price * room_count
            total = room_price * days

            hotel = Hotel.objects.get(id=id)

        context = {
            "data": request.session['selection_data_obj'],
            "total_selected_items": len(request.session['selection_data_obj']),
            "total": total,
            "total_days": total_days,
            "adult": adult,
            "children": children,
            "checkin": checkin,
            "checkout": checkout,
            "hotel": hotel,
        }

        return render(request, "hotel/selected_rooms.html", context)
    else:
        messages.warning(request, "You haven't selected any room yet")
        return redirect("/")

    # return render(request, "hotel/selected_rooms.html")


# View to handle the checkout process for a booking
# This view manages the checkout process for a specific booking
# identified by the booking ID. It retrieves the booking details
# from the database and prepares them for rendering in the checkout
# template. If the request method is POST, it saves the updated
# booking information. The view also passes the Stripe public key
# to the template for payment processing, facilitating the payment
# workflow.
def checkout(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    if request.method == "POST":

        booking.save()
        return redirect("hotel:checkout", booking.booking_id)

    context = {
        "booking": booking,
        "stripe_publishble_key": settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, "hotel/checkout.html", context)


# View to create a Stripe checkout session for a booking
# This view handles the creation of a Stripe checkout session for
# the specified booking. It retrieves the booking information and
# sets up the session with customer details and payment information.
# Upon successful creation of the session, it updates the booking
# status and returns the session ID as a JSON response, allowing
# the frontend to redirect the user to the Stripe payment page.
@csrf_exempt
def create_checkout_session(request, booking_id):
    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=booking.email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'USD',
                        'product_data': {
                            'name': f"Booking for {booking.full_name}",
                        },
                        # Stripe expects amount in cents
                        'unit_amount': int(booking.total * 100),
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse("hotel:success", args=[booking.booking_id])
            ) + f"?session_id={{CHECKOUT_SESSION_ID}}&success_id={booking.success_id}&booking_total={booking.total}",
            cancel_url=request.build_absolute_uri(
                reverse("hotel:failed", args=[booking.booking_id])
            )
        )

        # Update the booking status
        booking.payment_status = "Processing"
        booking.stripe_payment_intent = checkout_session['id']
        booking.save()

        return JsonResponse({"sessionId": checkout_session.id})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# View to handle successful payments after a booking.
# This view processes payment success after a user
# completes a booking. It retrieves the booking ID,
# success ID, and booking total from the GET parameters.
# If valid, it fetches the corresponding Booking object
# and verifies if the payment matches the recorded total.
# If confirmed, it updates the booking status to "Paid"
# and cleans up session data before rendering the success template.
def payment_success(request, booking_id):
    success_id = request.GET.get('success_id')
    booking_total = request.GET.get('booking_total')

    # booking = None
    print("booking_id =========", booking_id)

    if success_id and booking_total:
        success_id = success_id.rstrip("/")
        booking_total = booking_total.rstrip("/")

        booking = Booking.objects.get(
            booking_id=booking_id, success_id=success_id)

        if booking.total == Decimal(booking_total):
            print("Booking total matched.")
            if booking.payment_status == "Processing":
                booking.payment_status = "Paid"
                booking.is_active = True
                booking.save()

                if 'selection_data_obj' in request.session:
                    del request.session['selection_data_obj']

            else:
                messages.success(
                    request, "Payment has already been made. Thank you for your patronage.")
                # return redirect("/")
        else:
            messages.error(
                request, "Error: Payment manipulation detected.")

    context = {
        "booking": booking
    }
    # print("success_id ==", success_id)
    # print("booking_total ==", booking_total)

    return render(request, "hotel/payment_success.html", context)


# View to handle failed payments for a booking
# This view is triggered when a payment attempt for a booking fails.
# It retrieves the booking associated with the provided booking ID
# and updates its payment status to "failed." This allows the
# application to keep track of failed payment attempts and can
# inform users of the need to try again. The view then renders
# the payment failed template, providing feedback to the user.
def payment_failed(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    booking.payment_status = "failed"
    booking.save()

    context = {
        "booking": booking,
    }
    return render(request, "hotel/payment_failed.html", context)


# View to update room availability based on booking status.
# It checks active "Paid" bookings and updates the check-in
# and check-out statuses based on the current date. Rooms
# are marked available or unavailable depending on whether
# the booking has checked in or out. This ensures accurate
# room availability, reflecting the current state of the rooms.
@csrf_exempt
def update_room_status(request):
    today = timezone.now().date()

    booking = Booking.objects.filter(is_active=True, payment_status="Paid")
    for b in booking:
        if b.checked_in_tracker != True:
            if b.check_in_date > today:
                b.checked_in_tracker = False
                b.checked_in = False
                b.save()

                for r in b.room.all():
                    r.is_availble = True
                    r.save()

            else:
                b.checked_in_tracker = True
                b.checked_in = True
                b.save()

                for r in b.room.all():
                    r.is_availble = False
                    r.save()

        else:
            if b.check_out_date > today:
                b.checked_out_tracker = False
                b.checked_in = False
                b.save()

                for r in b.room.all():
                    r.is_available = False
                    r.save()

            else:
                b.checked_out_tracker = True
                b.checked_in = True
                b.save()

                for r in b.room.all():
                    r.is_available = True
                    r.save()

    return HttpResponse(today)
