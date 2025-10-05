from django.urls import path

from modules.playbooks.views import playbook_list_view, playbook_detail_view, playbook_create_view

urlpatterns = [
    path("", playbook_list_view, name="playbook_list"),
    path("create/", playbook_create_view, name="playbook_create"),
    path("detail/<int:playbook_id>", playbook_detail_view, name="playbook_detail"),
]