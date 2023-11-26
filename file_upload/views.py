from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ImageSerializer
from .models import UploadImage
from rest_framework import status
from django.http import FileResponse
import os
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/images/',
        '/images/uploads',
        '/images/view-image/<str:image_name>/'
    ]

    return Response(routes)


class ImageUploadView(APIView):
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ImageView(APIView):
    def get(self, request, image_name):
        try:
            image = UploadImage.objects.get(image=f'images/{image_name}')
        except UploadImage.DoesNotExist:
            return Response({'detail': 'image not found'}, status=status.HTTP_404_NOT_FOUND)

        image_path = image.image.path
        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')


class DeleteImageView(APIView):
    def delete(self, request, image_name):
        image = UploadImage.objects.filter(image=f'images/{image_name}')

        try:
            image = self.get_object(image_name)
        except UploadImage.DoesNotExist:
            return Response({'detail': 'image not found'}, status=status.HTTP_404_NOT_FOUND)

        image_path = image.image.path
        image.delete()  # Delete from the database
        os.remove(image_path)  # Delete from the directory

        return Response({'detail': 'image deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self, image_name):
        return UploadImage.objects.get(image=f'images/{image_name}')
