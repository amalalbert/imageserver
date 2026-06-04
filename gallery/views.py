from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Photo
from .serializers import PhotoSerializer

@api_view(['GET'])
def get_photo_urls(request):
    photos = Photo.objects.all()
    serializer = PhotoSerializer(photos, many=True, context={'request': request})
    
    # Extract just the string URLs from the objects to make a flat list
    # Result: ["http://192.168.1.5:8000/media/photos/img1.jpg", ...]
    url_list = [item['image_url'] for item in serializer.data]
    
    return Response(url_list)
