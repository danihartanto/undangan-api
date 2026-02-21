from rest_framework import serializers
from .models import Invitation, Guest


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = "__all__"
        read_only_fields = ("id", "user", "slug", "created_at", "updated_at")

class PublicInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = (
            "title",
            "event_type",
            "description",
            "event_date",
            "location",
            "google_maps_link",
            "slug",
        )

class GuestSerializer(serializers.ModelSerializer):
    invitation_link = serializers.SerializerMethodField()
    whatsapp_link = serializers.SerializerMethodField()

    class Meta:
        model = Guest
        fields = "__all__"
        read_only_fields = ("id", "guest_slug", "created_at", "updated_at")

    def get_invitation_link(self, obj):
        return obj.get_invitation_link()

    def get_whatsapp_link(self, obj):
        return obj.get_whatsapp_link()

# GET /api/invitations/guests/
# Response akan berisi:
# {
#   "name": "Budi Santoso",
#   "phone": "628123456789",
#   "guest_slug": "budi-santoso-a82k19",
#   "invitation_link": "http://localhost:3000/invitation/wedding-andi-sari/budi-santoso-a82k19/",
#   "whatsapp_link": "https://wa.me/628123456789?text=Assalamu..."
# }
        
class PublicRSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = (
            "name",
            "phone",
            "rsvp_status",
            "message",
            "guest_count",
        )

class PublicGuestInvitationSerializer(serializers.ModelSerializer):
    invitation_title = serializers.CharField(source="invitation.title")
    event_date = serializers.DateField(source="invitation.event_date")
    akad_time = serializers.TimeField(source="invitation.akad_time")
    reception_start_time = serializers.TimeField(source="invitation.reception_start_time")
    reception_end_time = serializers.TimeField(source="invitation.reception_end_time")
    location = serializers.CharField(source="invitation.location")
    description = serializers.CharField(source="invitation.description")
    google_maps = serializers.CharField(source="invitation.google_maps_link")

    class Meta:
        model = Guest
        fields = (
            "name",
            "address",
            "rsvp_status",
            "invitation_title",
            "description",
            "event_date",
            "akad_time",
            "reception_start_time",
            "reception_end_time",
            "location",
            "google_maps"
        )