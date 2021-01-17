import random
import time

from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Account, Transaction


def random_delay() -> int:
    # Simulate random factors and this one stupid network call that
    # I was making for realtime related stuff (should have been put
    # in a queue and delegated to a worker process).
    time.sleep(random.randint(3, 10))


@csrf_exempt  # Only because this is a quick and simple demo!
def ugly(request: HttpRequest) -> HttpResponse:
    try:
        account_id = int(request.POST["account"])
        amount = int(request.POST["amount"])
        if amount < 0:
            raise ValueError
    except (KeyError, ValueError):
        return HttpResponse(status=400)

    with transaction.atomic():
        try:
            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return HttpResponse(status=404)
        random_delay()
        account.balance += amount
        Transaction.objects.create(account=account, amount=amount)
        account.save()

    return HttpResponse(200)


@csrf_exempt  # Only because this is a quick and simple demo!
def bad(request: HttpRequest) -> HttpResponse:
    try:
        account_id = int(request.POST["account"])
        amount = int(request.POST["amount"])
        if amount < 0:
            raise ValueError
    except (KeyError, ValueError):
        return HttpResponse(status=400)

    with transaction.atomic():
        try:
            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return HttpResponse(status=404)
        account.balance += amount
        Transaction.objects.create(account=account, amount=amount)
        account.save()

    return HttpResponse(200)


@csrf_exempt  # Only because this is a quick and simple demo!
def good(request: HttpRequest) -> HttpResponse:
    try:
        account_id = int(request.POST["account"])
        amount = int(request.POST["amount"])
        if amount < 0:
            raise ValueError
    except (KeyError, ValueError):
        return HttpResponse(status=400)

    with transaction.atomic():
        try:
            account = Account.objects.select_for_update().get(id=account_id)
            # Consider making this non-blocking to avoid a DOS. For the sake
            # of this demo though, this is good enough.
        except Account.DoesNotExist:
            return HttpResponse(status=404)
        random_delay()
        account.balance += amount
        Transaction.objects.create(account=account, amount=amount)
        account.save()

    return HttpResponse(200)
