# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from goods.models import Goods
from goods.serializers import GoodsSerializer
from .authentications import IsOwner


class RecordsViewModel(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    search_fields = ['name', 'location']
    permission_classes = (IsOwner, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Goods.objects.filter(create_by=user)
