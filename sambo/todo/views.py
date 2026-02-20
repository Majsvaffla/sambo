from uuid import UUID

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from sambo import honeypot

from . import components
from .forms import ItemForm
from .models import CheckList, CheckListItem


def _hx_redirect_to_check_list(list_identifier: UUID) -> HttpResponse:
    return HttpResponse(headers={"HX-Redirect": reverse("check_list", args=[list_identifier])})


def check_list(request: HttpRequest, list_identifier: UUID | None = None) -> HttpResponse:
    list_instance = get_object_or_404(CheckList.objects, identifier=list_identifier) if list_identifier else CheckList()

    if request.method == "GET":
        return HttpResponse(components.check_list(request, list_instance))

    if request.method == "POST":
        if list_identifier is None:
            if "name" not in request.POST:
                return HttpResponse(status=400)

            if honeypot.is_absent(request):
                return honeypot.respond()

            assert list_instance.pk is None
            list_instance.name = request.POST["name"]
            list_instance.save()
            return _hx_redirect_to_check_list(list_instance.identifier)

        if (form := ItemForm(request.POST or None)).is_valid():
            item_instance = form.save(commit=False)
            item_instance.list = list_instance
            item_instance.save()
            return HttpResponse(components.item(item_instance))
        return HttpResponse(status=400)

    return HttpResponse(status=405)


def check_list_item(request: HttpRequest, list_identifier: UUID, item_pk: int) -> HttpResponse:
    item_instance = get_object_or_404(CheckListItem.objects, pk=item_pk, list__identifier=list_identifier)

    if request.method == "DELETE":
        item_instance.delete()
        return HttpResponse(components.items(item_instance.list))

    if request.method == "POST":
        if (form := ItemForm(request.POST or None, instance=item_instance)).is_valid():
            item_instance = form.save()
            return HttpResponse(components.item(item_instance))
        return HttpResponse(status=400)

    return HttpResponse(status=405)
