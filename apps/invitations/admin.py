from django.contrib import admin

# Register your models here.
from .models import Invitation, Guest


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "event_type",
        "user",
        "event_date",
        "akad_time",
        "reception_start_time",
        "reception_end_time",
        "is_published",
        "created_at",
    )

    list_filter = (
        "event_type",
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
        "user__email",
        "user__full_name",
    )

    readonly_fields = (
        "id",
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "id",
                "user",
                "event_type",
                "title",
                "slug",
                "description",
            )
        }),
        ("Event Details", {
            "fields": (
                "event_date",
                "akad_time",
                "reception_start_time",
                "reception_end_time",
                "location",
                "google_maps_link",
            )
        }),
        ("Publishing", {
            "fields": (
                "is_published",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "invitation",
        "rsvp_status",
        "phone",
        "invitation_link_display",
        "get_whatsapp_link",
        "created_at",
    )

    readonly_fields = (
        "id",
        "guest_slug",
        "invitation_link_display",
        "whatsapp_link_display",
        "created_at",
        "updated_at",
    )

    def invitation_link_display(self, obj):
        return obj.get_invitation_link()
    invitation_link_display.short_description = "Invitation Link"

    def whatsapp_link_display(self, obj):
        return obj.get_whatsapp_link()
    whatsapp_link_display.short_description = "WhatsApp Link"