from django.contrib import admin

from .models.playbook import Playbook

@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    list_display = ("name", "is_public")
    search_fields = ("name", "description")
    list_filter = ("is_public", "tags", "visible_to")
    filter_horizontal = ("tags", "visible_to")

