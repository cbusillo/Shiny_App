"""View for API access to Shiny Stuff"""
import locale
import socket
from django.core.handlers.wsgi import WSGIRequest  # type: ignore
from django.shortcuts import render  # type: ignore
from shiny_api.classes.ls_workorder import Workorder
from shiny_api.modules.load_config import Config
from shiny_api.modules.label_print import print_text
from shiny_api.modules.ring_central import send_message_ssh as send_message


def workorder_label(request: WSGIRequest):
    """print a label for a workorder"""
    context = {}
    password = ""
    quantity = int(request.GET.get("quantity", 1))
    workorder_id = int(request.GET.get("workorderID", 0))
    if workorder_id == 0:
        context["title"] = "No workorder ID"
        return render(request, "api/error.html", context)
    workorder = Workorder(workorder_id)
    for line in workorder.note.split("\n"):
        if line[0:2].lower() == "pw" or line[0:2].lower() == "pc":
            password = line
    print_text(
        f"{workorder.customer.first_name} {workorder.customer.last_name}",
        barcode=f"2500000{workorder.workorder_id}",
        quantity=quantity,
        text_bottom=password,
        print_date=True,
    )
    if str(request.GET.get("manual")).lower() != "true":
        context["auto_close"] = "True"
    return render(request, "api/close_window.html", context)


def ring_central_send_message(request: WSGIRequest):
    """Web listener to generate messages and send them via text"""
    context = {}

    workorder = Workorder(int(request.GET.get("workorderID", 0)))
    mobile_number = None

    for phone in workorder.customer.contact.phones.contact_phone:
        if phone.use_type == "Mobile":
            mobile_number = phone.number
    if mobile_number is None:
        context["title"] = "No mobile number"
        return render(request, "api/error.html", context)
    message_number = int(request.GET.get("message", 0))
    if workorder.total == 0 and request.GET.get("message") == "2":  # if we send a message with price with $0 price
        message_number += 1
    item_description = workorder.item_description
    for word in Config.STYLIZED_NAMES:
        if word.lower() in item_description.lower() and word not in item_description:
            index = item_description.lower().find(word.lower())
            item_description = item_description[:index] + word + item_description[index + len(word) :]

    message = Config.RESPONSE_MESSAGES[message_number]
    message = message.format(
        name=workorder.customer.first_name,
        product=item_description,
        total=locale.currency(workorder.total),
    )
    ip_address = request.META.get("REMOTE_ADDR")
    if ip_address is None:
        context["title"] = "No IP address"
        return render(request, "api/error.html", context)

    hostname = socket.gethostbyaddr(ip_address)[0]

    send_message(mobile_number, message, hostname)
    if str(request.GET.get("manual")).lower() != "true":
        context["auto_close"] = "True"

    return render(request, "api/close_window.html", context)
