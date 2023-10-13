from applications.profiles.views import ChangeProfilePhotoView , ChangeCoverPhotoView,ChangePrivacityView,ViewProflieView
from django.urls import path

urlpatterns = [
    path('<pk>/', ViewProflieView.as_view(), name='ver_prefil'),
    path('profile_photo/', ChangeProfilePhotoView.as_view(), name='cambiar_foto'),
    path('cover_photo/', ChangeCoverPhotoView.as_view(), name='cambiar_portada'),
    path('privacity/', ChangePrivacityView.as_view(), name='cambiar_privacidad'),
    
]