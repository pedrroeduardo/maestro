from django.urls import path

from modules.playbooks.views import playbook_list_view, playbook_update_view, playbook_create_view, playbook_delete_view

urlpatterns = [
    path("", playbook_list_view, name="playbook_list"),
    path("create/", playbook_create_view, name="playbook_create"),
    path("update/<int:playbook_id>", playbook_update_view, name="playbook_update"),
    path("delete/<int:playbook_id>", playbook_delete_view, name="playbook_delete"),
]