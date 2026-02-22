from django.contrib import admin

# Register your models here.
from .models import Invitation, Guest
from django.utils.html import format_html

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
        "invitation_link",
        "invitation_link_display",
        "whatsapp_link_display",
        "created_at",
    )

    readonly_fields = (
        "id",
        "guest_slug",
        "invitation_link",
        "invitation_link_display",
        "whatsapp_link_display",
        "created_at",
        "updated_at",
    )

    def invitation_link(self, obj):
        return obj.get_invitation_link()
    invitation_link.short_description = "Invitation Link"

    # def whatsapp_link_display(self, obj):
    #     return obj.get_whatsapp_link()
    # whatsapp_link_display.short_description = "WhatsApp Link"
    
    def invitation_link_display(self, obj):
        hard_url = "paynem.com"
        link = obj.get_invitation_link()
        # return f"{base_url}/invitations/invit_page.html?/{self.invitation.slug}/{self.guest_slug}/"
        # return f"{hard_url}/invitations/invit_page.html?{obj.invitation.slug}/{obj.guest_slug}/"
        return format_html(
            '<a class="button" style="background:#0096c7;color:white;padding:4px 8px;border-radius:4px;" href="{}" target="_blank">🌐 Open</a>',
            link
        )
    
    invitation_link_display.short_description = "Invitation Link Display"

    
    
    def whatsapp_link_display(self, obj):
        link = obj.get_whatsapp_link()
        if not link:
            return "-"
        return format_html(
            '<a class="button" style="background:#25D366;color:white;padding:4px 8px;border-radius:4px;" href="{}" target="_blank">📲 Send</a>',
            link
        )
    whatsapp_link_display.short_description = "WhatsApp Link"
    