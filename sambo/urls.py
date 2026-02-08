from django.urls import include, path

from . import admin, views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("todo/", include("sambo.todo.urls")),
    path("expense/", include("sambo.expense.urls")),
]
