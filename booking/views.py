from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from hotel.models import Hotel, Room, RoomType, HotelGallery, HotelFeatures, Booking
from datetime import datetime
from django.template.loader import render_to_string


# View to check room availability based on the user's selection
@csrf_exempt
def check_room_availability(request):
    if request.method == "POST":
        id = request.POST.get("hotel-id")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        adult = request.POST.get("adult")
        children = request.POST.get("children")
        room_type = request.POST.get("room-type")

        # print("hotel ==== ", hotel)
        # print("room_type ==== ", room_type)

        hotel = Hotel.objects.get(status="Live", id=id)
        room_type = RoomType.objects.get(hotel=hotel, slug=room_type)

        print("id ==== ", id)
        print("checkin ==== ", checkin)
        print("checkout ==== ", checkout)
        print("adult ==== ", adult)
        print("children ==== ", children)
        print("room_type ==== ", room_type)
        print("hotel ==== ", hotel)
        print("room_type ==== ", room_type)

        url = reverse("hotel:room_type_detail", args=[
                      hotel.slug, room_type.slug])
        url_with_params = f"{url}?hotel-id={id}&checkin={checkin}&checkout={checkout}&adult={adult}&children={children}&room_type={room_type}"
        return HttpResponseRedirect(url_with_params)


# View to add a room to the user's selection (stored in the session)
def add_to_selection(request):
    room_selection = {}
    # room_selectiondoesnotexists
    room_selection[str(request.GET['id'])] = {
        'hotel_id': request.GET['hotel_id'],
        'hotel_name': request.GET['hotel_name'],
        'room_name': request.GET['room_name'],
        'room_price': request.GET['room_price'],
        'number_of_beds': request.GET['number_of_beds'],
        'room_number': request.GET['room_number'],
        'room_type': request.GET['room_type'],
        'room_id': request.GET['room_id'],
        'checkout': request.GET['checkout'],
        'checkin': request.GET['checkin'],
        'adult': request.GET['adult'],
        'children': request.GET['children'],
    }

    if 'selection_data_obj' in request.session:
        # if "1" in "room_selection1, room_selection2, room_selection3":
        if str(request.GET['id']) in request.session['selection_data_obj']:
            selection_data = request.session['selection_data_obj']
            selection_data[str(request.GET['id'])]['adult'] = int(
                room_selection[str(request.GET['id'])]['adult'])
            selection_data[str(request.GET['id'])]['children'] = int(
                room_selection[str(request.GET['id'])]['children'])
            request.session['selection_data_obj'] = selection_data
        else:
            selection_data = request.session['selection_data_obj']
            selection_data.update(room_selection)
            request.session['selection_data_obj'] = selection_data
    else:
        request.session['selection_data_obj'] = room_selection

    data = {
        "data": request.session['selection_data_obj'],
        "total_selected_items": len(request.session['selection_data_obj'])
    }

    return JsonResponse(data)


# View to delete all room selections from the session
def delete_session(request):
    request.session.pop('selection_data_obj', None)
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete a specific room selection from the session
def delete_selection(request):
    # hotel_id = str(request.Get.get(id)])
    hotel_id = str(request.GET['id'])

    if 'selection_data_obj' in request.session:
        if hotel_id in request.session['selection_data_obj']:
            selection_data = request.session['selection_data_obj']
            del request.session['selection_data_obj'][hotel_id]
            request.session['selection_data_obj'] = selection_data

    total = 0
    room_count = 0
    total_days = 0
    adult = 0
    children = 0
    checkin = ""
    checkout = ""
    hotel = None

    if 'selection_data_obj' in request.session:
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

            # hotel = Hotel.objects.get(id=id)

    context = render_to_string(
        "hotel/async/selected_room.html",
        {
            "data": request.session['selection_data_obj'],
            "total_selected_item": len(request.session['selection_data_obj']),
            "total": total,
            "total_days": total_days,
            "adult": adult,
            "children": children,
            "checkin": checkin,
            "checkout": checkout,
            "hotel": hotel,
        }
    )

    print("context =======", context)
    return JsonResponse({"data": context, "total_selected_item": len(request.session['selection_data_obj'])})
