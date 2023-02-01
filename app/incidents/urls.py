from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView
from incidents.views import home
from incidents import views 
from .features import HAS_TASK_MERGE

urlpatterns = (
    [
        #path("", TemplateView.as_view(template_name="home.html"), name="home"),
        path("", home.dashboard_functions, name="home"),
        path("profile", TemplateView.as_view(template_name="home/profile.html"), name="profile"),
        path("login", auth_views.LoginView.as_view(), name="login"),
        path("logout", auth_views.LogoutView.as_view(), name="logout"),
        path("gtdadmin/", admin.site.urls),
        #path("todo/", include("todo.urls", namespace="todo")),
        path("lists", views.list_lists, name="lists"),
        # View reorder_tasks is only called by JQuery for drag/drop task ordering.
        path("reorder_tasks/", views.reorder_tasks, name="reorder_tasks"),
        # Allow users to post tasks from outside django-todo (e.g. for filing tickets - see docs)
        path("ticket/add/", views.external_add, name="external_add"),
        # Three paths into `list_detail` view
        path("mine/", views.list_detail, {"list_slug": "mine"}, name="mine"),
        path(
                "<int:list_id>/<str:list_slug>/completed/",
                views.list_detail,
                {"view_completed": True},
                name="list_detail_completed",),
        path("<int:list_id>/<str:list_slug>/", views.list_detail, name="list_detail"),
        path("<int:list_id>/<str:list_slug>/delete/", views.del_list, name="del_list"),
        path("add_list/", views.add_list, name="add_list"),
        path("task/<int:task_id>/", views.task_detail, name="task_detail"),
        path(
            "attachment/remove/<int:attachment_id>/", views.remove_attachment, name="remove_attachment"
            ),    
    ]
    # Static media in DEBUG mode:
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if HAS_TASK_MERGE:
    # ensure mail tracker autocomplete is optional
    from incidents.views.task_autocomplete import TaskAutocomplete

    urlpatterns.append(
        path(
            "task/<int:task_id>/autocomplete/", TaskAutocomplete.as_view(), name="task_autocomplete"
        )
    )

urlpatterns.extend(
    [
        path("toggle_done/<int:task_id>/", views.toggle_done, name="task_toggle_done"),
        path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
        path("search/", views.search, name="search"),
        path("import_csv/", views.import_csv, name="import_csv"),
    ]
)
