from rest_framework import generics
from .models import History
from .serializers import HistorySerializer

class HistoryList(generics.ListAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
