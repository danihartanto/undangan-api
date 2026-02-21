from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Invitation, Guest
from .serializers import PublicInvitationSerializer, PublicRSVPSerializer, PublicGuestInvitationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


class PublicInvitationDetailView(RetrieveAPIView):
    serializer_class = PublicInvitationSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Invitation.objects.filter(is_published=True)

# class PublicRSVPView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, slug):
#         invitation = get_object_or_404(
#             Invitation,
#             slug=slug,
#             is_published=True
#         )

#         serializer = PublicRSVPSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(invitation=invitation)
#             return Response(
#                 {"message": "RSVP submitted successfully"},
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicRSVPView(APIView):

    def get_guest(self, guest_slug):
        try:
            return Guest.objects.get(slug=guest_slug)
        except Guest.DoesNotExist:
            return None

    def get(self, request, guest_slug):
        guest = self.get_guest(guest_slug)
        if not guest:
            return Response({"detail": "Guest not found"}, status=404)

        try:
            rsvp = Guest.objects.get(guest=guest)
            serializer = PublicRSVPSerializer(rsvp)
            return Response(serializer.data)
        except Guest.DoesNotExist:
            return Response({"detail": "RSVP not found"}, status=404)

    def post(self, request, guest_slug):
        guest = self.get_guest(guest_slug)
        if not guest:
            return Response({"detail": "Guest not found"}, status=404)

        if Guest.objects.filter(guest=guest).exists():
            return Response(
                {"detail": "RSVP already exists. Use PUT to update."},
                status=400
            )

        serializer = PublicRSVPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(guest=guest)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    def put(self, request, guest_slug):
        guest = self.get_guest(guest_slug)
        if not guest:
            return Response({"detail": "Guest not found"}, status=404)

        try:
            rsvp = Guest.objects.get(guest=guest)
        except Guest.DoesNotExist:
            return Response({"detail": "RSVP not found"}, status=404)

        serializer = PublicRSVPSerializer(rsvp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, guest_slug):
        guest = self.get_guest(guest_slug)
        if not guest:
            return Response({"detail": "Guest not found"}, status=404)

        try:
            rsvp = Guest.objects.get(guest=guest)
        except Guest.DoesNotExist:
            return Response({"detail": "RSVP not found"}, status=404)

        serializer = PublicRSVPSerializer(rsvp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

class PublicGuestInvitationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, invitation_slug, guest_slug):
        guest = get_object_or_404(
            Guest,
            invitation__slug=invitation_slug,
            guest_slug=guest_slug,
            invitation__is_published=True
        )

        # track open
        if not guest.is_opened:
            guest.is_opened = True
            guest.opened_at = timezone.now()
            guest.save()

        serializer = PublicGuestInvitationSerializer(guest)
        return Response(serializer.data)
    
class PublicGuestRSVPView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, invitation_slug, guest_slug):
        guest = get_object_or_404(
            Guest,
            invitation__slug=invitation_slug,
            guest_slug=guest_slug,
            invitation__is_published=True
        )
        if not guest:
            return Response({"detail": "Guest not found"}, status=404)

        try:
            rsvp = guest = get_object_or_404(
                Guest,
                invitation__slug=invitation_slug,
                guest_slug=guest_slug,
                invitation__is_published=True
            )
            serializer = PublicRSVPSerializer(rsvp)
            return Response(serializer.data)
        except Guest.DoesNotExist:
            return Response({"detail": "RSVP not found"}, status=404)

    def post(self, request, invitation_slug, guest_slug):
        guest = get_object_or_404(
            Guest,
            invitation__slug=invitation_slug,
            guest_slug=guest_slug,
            invitation__is_published=True
        )

        if guest.rsvp_status != "pending":
            return Response(
                {"error": "RSVP already submitted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        rsvp_status = request.data.get("rsvp_status")
        message = request.data.get("message")
        guest_count = request.data.get("guest_count", 1)

        guest.rsvp_status = rsvp_status
        guest.message = message
        guest.guest_count = guest_count
        guest.save()

        return Response({"message": "RSVP submitted successfully"})
    
    def patch(self, request, invitation_slug, guest_slug):
        try:
            guest = Guest.objects.get(
                guest_slug=guest_slug,
                invitation__slug=invitation_slug
            )
        except Guest.DoesNotExist:
            return Response({"detail": "Guest not found"}, status=404)

        try:
            rsvp = Guest.objects.get(guest_slug=guest_slug)
        except Guest.DoesNotExist:
            return Response({"detail": "RSVP not found"}, status=404)

        serializer = PublicRSVPSerializer(rsvp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)