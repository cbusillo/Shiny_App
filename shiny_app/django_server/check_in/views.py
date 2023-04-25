"""App to check customers in"""

from django.shortcuts import redirect, render


from shiny_app.modules.light_speed import import_customers

from ..customers.models import Customer


def home(request):
    """Render home page"""
    customers = Customer.objects.all().order_by("-update_time")[:100]
    if customers.count() == 0:
        return redirect("functions:home")
    import_customers()

    return render(request, "check_in/home.html")
