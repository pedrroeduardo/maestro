from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from modules.playbooks.forms import PlaybookForm
from modules.playbooks.models.playbook import Playbook

PAGINATE_BY = 20

class PlaybookListView(LoginRequiredMixin, ListView):
    model = Playbook
    template_name = "playbooks/playbook_list.html"
    context_object_name = "playbooks"
    paginate_by = PAGINATE_BY

    login_url = "login"
    redirect_field_name = "next"

    def get_queryset(self):
        user = self.request.user
        user_groups_ids = user.groups.values_list('id', flat=True)
        return (Playbook.objects
                .filter(Q(is_public=True) | Q(visible_to__in=user_groups_ids))
                .distinct()
                .order_by('name'))

playbook_list_view = PlaybookListView.as_view()

class PlaybookUpdateView(LoginRequiredMixin, UpdateView):
    model = Playbook
    template_name = "playbooks/playbook_detail.html"
    form_class = PlaybookForm
    context_object_name = "playbook"
    pk_url_kwarg = "playbook_id"

    login_url = "login"
    redirect_field_name = "next"
    success_url = reverse_lazy("playbook_list")

    def get_queryset(self):
        user = self.request.user
        user_groups_ids = user.groups.values_list('id', flat=True)
        return Playbook.objects.filter(Q(is_public=True) | Q(visible_to__in=user_groups_ids)).distinct()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_visible_to(self.request.user):
            raise PermissionDenied("You do not have permission to view this playbook.")
        return obj

playbook_update_view = PlaybookUpdateView.as_view()

class PlaybookCreateView(LoginRequiredMixin, CreateView):
    model = Playbook
    template_name = "playbooks/playbook_detail.html"
    form_class = PlaybookForm
    context_object_name = "playbook"
    pk_url_kwarg = "playbook_id"

    login_url = "login"
    redirect_field_name = "next"
    success_url = reverse_lazy("playbook_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

playbook_create_view = PlaybookCreateView.as_view()

class PlaybookDeleteView(LoginRequiredMixin, DeleteView):
    model = Playbook
    template_name = "playbooks/playbook_confirm_delete.html"
    context_object_name = "playbook"
    pk_url_kwarg = "playbook_id"

    login_url = "login"
    redirect_field_name = "next"
    success_url = reverse_lazy("playbook_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        self.object.delete()
        messages.success(self.request, f'Playbook "{name}" was deleted successfully.')
        return redirect(self.get_success_url())

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_visible_to(self.request.user):
            raise PermissionDenied("You do not have permission to delete this playbook.")
        return obj

playbook_delete_view = PlaybookDeleteView.as_view()
