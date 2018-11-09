from django.dispatch import Signal

# New bike has been added
bike_registered = Signal(providing_args=["bike", "request"])
