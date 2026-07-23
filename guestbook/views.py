from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import GuestMessage
from .serializers import GuestMessageSerializer


class GuestMessageViewSet(viewsets.ModelViewSet):
    queryset = GuestMessage.objects.all()
    serializer_class = GuestMessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
