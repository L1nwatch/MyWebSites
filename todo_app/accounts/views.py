# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import authenticate, login


def persona_login(request):
    user = authenticate(assertion=request.POST["assertion"])
    if user is not None:
        login(request, user)
    return HttpResponse("OK")

