# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from goods.models import Goods
from goods.serializers import GoodsSerializer


class RecordsViewModel(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    search_fields = ['name', 'location']
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)

