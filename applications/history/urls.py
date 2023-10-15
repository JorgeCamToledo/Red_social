from applications.history.views import HistoryList
from django.urls import path

urlpatterns = [
    path('', HistoryList.as_view(), name='ver historial'),
    
    
]