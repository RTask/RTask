from django.conf.urls import url
from.views import ticket_view

urlpatterns =[
    url('createticket', ticket_view, name='Current user'),  # get the current user
]
