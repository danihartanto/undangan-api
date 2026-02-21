from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Invitation, Guest
from .serializers import InvitationSerializer, GuestSerializer
from .permissions import IsOwner


class InvitationViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    # admin masih bisa edit invitation
    def get_queryset(self):
        return Invitation.objects.filter(user=self.request.user)
    
    # Kalau ingin admin tidak bisa edit invitation milik user lain, kita bisa tambahkan override:
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(user=request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GuestViewSet(viewsets.ModelViewSet):
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Guest.objects.filter(
            invitation__user=self.request.user
        )

    def perform_create(self, serializer):
        invitation = serializer.validated_data["invitation"]

        if invitation.user != self.request.user:
            raise self.permission_denied("Not allowed.")

        serializer.save()