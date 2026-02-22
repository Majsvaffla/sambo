from base64 import b64encode

import filetype  # type: ignore[import-untyped]
import htpy as h
from django.http import HttpRequest
from django.templatetags.static import static
from django.urls import reverse

from sambo import honeypot
from sambo.components import page
from sambo.share.models import Upload


def _page(request: HttpRequest, *content: h.Node, title: str) -> h.Element:
    return page(
        request,
        title=title,
        head=[
            h.link(rel="stylesheet", href=static("share/styles.css")),
            h.script(src=static("share/script.js")),
        ],
        main=h.main[content],
    )


def _toolbar(request: HttpRequest, upload_instance: Upload, *, is_image_rendered: bool, orientation: str) -> h.Element:
    relative_uploaded_url = reverse("uploaded", args=[upload_instance.identifier])
    url_for_sharing = request.build_absolute_uri(relative_uploaded_url)
    write_url_to_clipboard = f'navigator.clipboard.writeText("{url_for_sharing}")'
    button_variant = "neutral" if is_image_rendered else "brand"

    return h.wa_button_group(orientation=orientation, label="Alternativ")[
        h.wa_button(
            {"@click": write_url_to_clipboard},
            x_init=None if is_image_rendered else write_url_to_clipboard,
            variant=button_variant,
        )[
            h.wa_icon(name="copy", slot="start"),
            "Kopiera länken",
        ],
        h.wa_button(variant=button_variant, href=reverse("download", args=[upload_instance.identifier]))[
            h.wa_icon(name="download", slot="start"),
            "Ladda ner filen",
        ],
        is_image_rendered
        or h.wa_button(variant=button_variant, href=relative_uploaded_url)[
            h.wa_icon(name="image", slot="start"),
            "Öppna filen",
        ],
        h.wa_button(
            variant=button_variant,
            hx_delete=relative_uploaded_url,
            hx_vals=honeypot.as_json(),
            hx_target="main",
            hx_confirm="Vill du ta bort den uppladdade filen?",
        )[
            h.wa_icon(name="trash", slot="start"),
            "Kasta filen",
        ],
    ]


def _img(upload_instance: Upload) -> h.VoidElement:
    encoded_content = b64encode(upload_instance.content).decode("utf8")
    mime_type = filetype.guess(upload_instance.content)
    return h.img(src=f"data:{mime_type};charset=utf-8;base64,{encoded_content}")


def uploaded(request: HttpRequest, upload_instance: Upload, *, render_image: bool = False) -> h.Element:
    return h.section[
        render_image and _img(upload_instance),
        _toolbar(request, upload_instance, is_image_rendered=render_image, orientation="horizontal"),
        _toolbar(request, upload_instance, is_image_rendered=render_image, orientation="vertical"),
    ]


def drop_zone() -> h.Element:
    return h.section(
        "#drop-zone",
        {
            "@dragover": "handleDragover",
            "@drop.prevent": "handleFiles($event.dataTransfer.files, $refs.fileInput)",
            "@paste.window.prevent": "handleFiles($event.clipboardData.files, $refs.fileInput)",
            "@click": '$el.querySelector("input").click()',
        },
        x_data=r"{uploadHasStarted: false}",
    )[
        h.wa_progress_ring({"@htmx:xhr:progress.outside": "handleProgress"}, x_show="uploadHasStarted"),
        h.label(x_show="!uploadHasStarted")[
            "Släpp en fil eller klicka för att välja en fil att ladda upp.",
            h.input(
                {"@change": "uploadHasStarted = true"},
                x_ref="fileInput",
                name="file",
                type="file",
                accept="image/*",
                hx_post=reverse("upload"),
                hx_encoding="multipart/form-data",
                hx_trigger="change,drop from:#drop-zone,paste from:window",
                hx_vals=honeypot.as_json(),
                hx_target="main",
            ),
        ],
    ]


def uploaded_page(request: HttpRequest, upload_instance: Upload) -> h.Element:
    return _page(
        request,
        uploaded(request, upload_instance, render_image=True),
        title=upload_instance.name,
    )


def upload_page(request: HttpRequest) -> h.Element:
    return _page(request, drop_zone, title="Ladda upp en fil")
