import typing as t
from io import BytesIO
from uuid import UUID

import filetype  # type: ignore[import-untyped]
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from sambo import honeypot

from . import components
from .models import Upload

if t.TYPE_CHECKING:
    from django.core.files.uploadedfile import UploadedFile

MAXIMUM_FILE_SIZE_IN_BYTES = 10_000_000  # 10 MB


def upload(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return HttpResponse(components.upload_page(request))

    if request.method == "POST":
        if honeypot.is_absent(request):
            return honeypot.respond()

        if not request.FILES:
            return HttpResponse("Exactly one file must be uploaded at a time.", status=400)

        # Incompatible types in assignment (expression has type "Iterator[UploadedFile | list[object]]", variable has type "Sequence[UploadedFile]")  # noqa: E501
        files: t.Sequence[UploadedFile] = list(request.FILES.values())  # type: ignore[arg-type]
        if len(files) != 1:
            return HttpResponse("Exactly one file must be uploaded at a time.", status=400)

        [file] = files

        if not file.name:
            return HttpResponse("The uploaded file must have a name.", status=400)

        content = file.read()

        if not filetype.is_image(content):
            return HttpResponse("The uploaded file must be an image.", status=400)

        if MAXIMUM_FILE_SIZE_IN_BYTES < (file.size or 0) < 1:
            return HttpResponse(
                f"The size of the uploaded file must be at most {MAXIMUM_FILE_SIZE_IN_BYTES / 1_000_000} MB.",
                status=400,
            )

        upload_instance = Upload.objects.create(name=file.name, content=content)
        return HttpResponse(
            components.uploaded(request, upload_instance, copy_to_clipboard_on_load=True),
            headers={"HX-Push-Url": reverse("uploaded", args=[upload_instance.identifier])},
        )

    return HttpResponse(status=405)


def uploaded(request: HttpRequest, upload_identifier: UUID) -> HttpResponse:
    if request.method == "GET":
        return HttpResponse(components.uploaded_page(request, get_object_or_404(Upload, identifier=upload_identifier)))

    if request.method == "DELETE":
        Upload.objects.filter(identifier=upload_identifier).delete()
        return HttpResponse(
            components.drop_zone(),
            headers={"HX-Push-Url": reverse("upload")},
        )

    return HttpResponse(status=405)


def download(request: HttpRequest, upload_identifier: UUID) -> HttpResponse | FileResponse:
    if request.method == "GET":
        upload_instance = get_object_or_404(Upload, identifier=upload_identifier)
        return FileResponse(BytesIO(upload_instance.content), filename=upload_instance.name, as_attachment=True)

    return HttpResponse(status=405)
