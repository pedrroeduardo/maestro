from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from modules.core.models import Tag, GroupMember, Group
from modules.users.models import CustomUser


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")

    exclude = ("created_by", "updated_by", "deleted_by", "deleted_at")

class GroupMemberInlineForUser(admin.TabularInline):
    model = GroupMember
    fk_name = "user"
    extra = 1
    autocomplete_fields = ("group",)

    exclude = ("created_by", "updated_by", "deleted_by", "deleted_at")


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    inlines = [GroupMemberInlineForUser]

    exclude = ("created_by", "updated_by", "deleted_by", "deleted_at")

class GroupMemberInlineForGroup(admin.TabularInline):
    model = GroupMember
    fk_name = "group"
    extra = 1
    autocomplete_fields = ("user",)

    exclude = ("created_by", "updated_by", "deleted_by", "deleted_at")



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [GroupMemberInlineForGroup]

    exclude = ("created_by", "updated_by", "deleted_by", "deleted_at")
