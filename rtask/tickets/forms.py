
# brightness_5
# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import Ticket
class TicketForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Ticket
        fields = "__all__"