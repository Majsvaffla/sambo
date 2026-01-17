from django.urls import include, path

from . import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("todo/", include("sambo.todo.urls")),
]
