from django.shortcuts import render

# Create your views her
from django.shortcuts import render
from .forms import TicketForm


def ticket_view(request):
    context = {}

    # create object of form
    form = TicketForm(request.POST or None, request.FILES or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()

    context['form'] = form
    return render(request, "ticket.html", {'form': form})
