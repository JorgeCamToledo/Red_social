from rest_framework_simplejwt.views import TokenObtainPairView
from applications.authentication.views import RegistrationView
from django.urls import path

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegistrationView.as_view(), name='register'),
    
]