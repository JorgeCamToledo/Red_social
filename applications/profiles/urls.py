from applications.profiles.views import ChangeProfilePhotoView , ChangeCoverPhotoView,ChangePrivacityView,ViewProflieView
from django.urls import path

urlpatterns = [
    path('<pk>/', ViewProflieView.as_view(), name='ver_prefil'),
    path('photo/profile/', ChangeProfilePhotoView.as_view(), name='cambiar_foto'),
    path('photo/cover/', ChangeCoverPhotoView.as_view(), name='cambiar_portada'),
    path('change/privacity/', ChangePrivacityView.as_view(), name='cambiar_privacidad'),
    
]