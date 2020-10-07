# import form class from django
from django import forms

# import Ticket from models.py
from .models import Ticket
class TicketForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Ticket
        fields = "__all__"