from rest_framework.routers import DefaultRouter
from .views import InvitationViewSet, GuestViewSet
from .public_views import PublicInvitationDetailView, PublicRSVPView, PublicGuestInvitationView, PublicGuestRSVPView
from django.urls import path

router = DefaultRouter()
router.register(r'', InvitationViewSet, basename='invitation')
router.register(r'guests', GuestViewSet, basename='guest')
# urlpatterns = router.urls


urlpatterns = router.urls + [
    path(
        "public/<slug:slug>/",
        PublicInvitationDetailView.as_view(),
        name="public-invitation-detail",
    ),
    
    # GET /api/invitations/public/{slug}/
    # contoh => GET /api/invitations/public/wedding-andi-sari-a82k19dl/
]
urlpatterns += [
    # path(
    #     "public/<slug:slug>/rsvp/",
    #     PublicRSVPView.as_view(),
    #     name="public-rsvp",
    # ),
    path(
    "public/<slug:slug>/rsvp/",
    PublicRSVPView.as_view(),
    name="public-rsvp"
),
    # POST /api/invitations/public/{slug}/rsvp/
    # {
    #     "name": "Budi",
    #     "phone": "08123456789",
    #     "rsvp_status": "attending",
    #     "message": "Selamat ya semoga bahagia!",
    #     "guest_count": 2
    # }
]

urlpatterns += [
    path(
        "public/<slug:invitation_slug>/<slug:guest_slug>/",
        PublicGuestInvitationView.as_view(),
    ),
    path(
        "public/<slug:invitation_slug>/<slug:guest_slug>/rsvp/",
        PublicGuestRSVPView.as_view(),
    ),
    
    # GET /api/invitations/public/{invitation_slug}/{guest_slug}/
    # {
    #     "name": "Budi Santoso",
    #     "address": "Jl. Mawar No. 10 Jakarta",
    #     "rsvp_status": "pending",
    #     "invitation_title": "Wedding Andi & Sari",
    #     "description": "...",
    #     "event_date": "2026-03-01T10:00:00Z",
    #     "location": "Hotel Mulia Jakarta"
    # }
]