from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from . import components
from .forms import ItemForm
from .models import CheckListItem, CheckList


def check_list(request: HttpRequest, list_identifier: UUID) -> HttpResponse:
    list_instance = get_object_or_404(CheckList.objects, identifier=list_identifier)

    if request.method == "GET":
        return HttpResponse(components.check_list(request, list_instance))

    if request.method == "POST":
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
