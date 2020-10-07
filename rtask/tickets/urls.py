from django.conf.urls import url
from.views import ticket_view

urlpatterns =[
    url('createticket', ticket_view, name='Create Ticket'),  # create ticket
]
