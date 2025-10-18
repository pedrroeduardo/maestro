from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from modules.core.models import Tag, GroupMember, Group
from modules.users.models import CustomUser


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")


class GroupMemberInlineForUser(admin.TabularInline):
    model = GroupMember
    fk_name = "user"
    extra = 1
    autocomplete_fields = ("group",)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    inlines = [GroupMemberInlineForUser]


class GroupMemberInlineForGroup(admin.TabularInline):
    model = GroupMember
    fk_name = "group"
    extra = 1
    autocomplete_fields = ("user",)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [GroupMemberInlineForGroup]
