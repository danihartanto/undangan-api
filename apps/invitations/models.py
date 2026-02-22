from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid
import urllib.parse
import re

class Invitation(models.Model):
    EVENT_TYPE_CHOICES = (
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invitations"
    )

    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField(blank=True, null=True)

    event_date = models.DateField()
    
    akad_time = models.TimeField(blank=True, null=True)
    reception_start_time = models.TimeField(blank=True, null=True)
    reception_end_time = models.TimeField(blank=True, null=True)
    
    location = models.CharField(max_length=255)
    google_maps_link = models.URLField(blank=True, null=True)

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Guest(models.Model):
    RSVP_STATUS = (
        ("pending", "Pending"),
        ("attending", "Attending"),
        ("not_attending", "Not Attending"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    invitation = models.ForeignKey(
        Invitation,
        on_delete=models.CASCADE,
        related_name="guests"
    )

    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=28, blank=True, null=True)  # WA number

    guest_slug = models.SlugField(unique=True, blank=True)

    rsvp_status = models.CharField(
        max_length=20,
        choices=RSVP_STATUS,
        default="pending"
    )

    message = models.TextField(blank=True, null=True)
    guest_count = models.PositiveIntegerField(default=1)

    is_opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.guest_slug:
            self.guest_slug = (
                slugify(self.name) + "-" + str(uuid.uuid4())[:6]
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.invitation.title}"
    
    def get_invitation_link(self):
        base_url = getattr(settings, "FRONTEND_URL", "http://127.0.0.1:5500")
        hard_url = "https://paynem.com"
        # return f"{base_url}/invitations/invit_page.html?/{self.invitation.slug}/{self.guest_slug}/"
        # return f"{hard_url}/invitations/invit_page.html?{self.invitation.slug}/{self.guest_slug}/"
        return f"{hard_url}/invitations/invit_page.html?{self.invitation.slug}/{self.guest_slug}/"


    def get_whatsapp_link(self):
        if not self.phone:
            return None

        # clean_phone = self.phone.replace("-", "").replace(" ", "")
        clean_phone = self.validate_whatsapp_number(self.phone)

        message = (
            f"Assalamu'alaikum Wr. Wb. \n\n Yth. *{self.name}*,\n\n"
            f"Kami mengundang Anda untuk menghadiri acara pernikahan kami:\n"
            f"{self.invitation.title}\n\n"
            f"Kami berharap akan kehadiran bapak/ibu/sahabat di hari bahagia kami.\n"
            f"Untuk detail waktu dan lokasi silakan buka link berikut:\n"
            f"{self.get_invitation_link()}"
        )

        
        encoded_message = urllib.parse.quote(message)

        return f"https://wa.me/{clean_phone}?text={encoded_message}"

    def validate_whatsapp_number(self, value):
        if not value:
            return value

        # Hapus semua kecuali angka dan +
        value = re.sub(r'[^0-9+]', '', value)

        if value.startswith('08'):
            value = '+62' + value[1:]

        elif value.startswith('62'):
            value = '+' + value

        elif not value.startswith('+'):
            value = '+62' + value

        return value