from django.urls import path
from .views import getRoutes, ImageUploadView, ImageView, DeleteImageView

urlpatterns = [
    path('', getRoutes, name='routes'),
    path('uploads/', ImageUploadView.as_view(), name='upload'),
    path('view-image/<str:image_name>/', ImageView.as_view(), name='image-view'),
    path('<str:image_name>/delete-image/',
         DeleteImageView.as_view(), name='image-delete'),
]
