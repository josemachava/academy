from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import FooterColumn, FooterLink, FooterPodcast, FooterSettings, FooterSocial, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["-date_joined"]
    list_display = ["email", "first_name", "last_name", "is_staff", "is_active", "date_joined"]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["email", "first_name", "last_name"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ["date_joined", "last_login"]

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    # Required by BaseUserAdmin — map to our email-based model
    filter_horizontal = ("groups", "user_permissions")


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    ordering = ["order", "id"]


@admin.register(FooterPodcast)
class FooterPodcastAdmin(admin.ModelAdmin):
    list_display = ["heading", "spotify_url", "google_podcasts_url", "updated_at"]


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    list_editable = ["order"]
    ordering = ["order", "id"]
    inlines = [FooterLinkInline]


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ["title", "column", "url", "order"]
    list_filter = ["column"]
    list_editable = ["order"]
    ordering = ["column__order", "order", "id"]


@admin.register(FooterSocial)
class FooterSocialAdmin(admin.ModelAdmin):
    list_display = ["platform", "url", "order"]
    list_editable = ["order", "url"]
    ordering = ["order", "id"]


@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    list_display = ["__str__", "copyright_text", "copyright_text_en"]
