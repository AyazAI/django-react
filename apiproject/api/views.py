from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from api.models import Text
from api.serializers import TextSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def text_list(request):
    # GET list of api, POST a new text, DELETE all api
    if request.method == 'GET':
        text = Text.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            text = text.filter(title__icontains=title)
        
        text_serializer = TextSerializer(text, many=True)
        return JsonResponse(text_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        text_data = JSONParser().parse(request)
        text_serializer = TextSerializer(data=text_data)
        if text_serializer.is_valid():
            text_serializer.save()
            return JsonResponse(text_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(text_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Text.objects.all().delete()
        return JsonResponse({'message': '{} Texts were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

 
 
@api_view(['GET', 'PUT', 'DELETE'])
def text_detail(request, pk):
    # find text by pk (id)
    try: 
        text = Text.objects.get(pk=pk) 
    except Text.DoesNotExist: 
        return JsonResponse({'message': 'The text does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE text
    if request.method == 'GET': 
        text_serializer = TextSerializer(text) 
        return JsonResponse(text_serializer.data) 

    elif request.method == 'PUT': 
        text_data = JSONParser().parse(request) 
        text_serializer = TextSerializer(text, data=text_data) 
        if text_serializer.is_valid(): 
            text_serializer.save() 
            return JsonResponse(text_serializer.data) 
        return JsonResponse(text_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        text.delete() 
        return JsonResponse({'message': 'Text was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        
        
@api_view(['GET'])
def text_list_published(request):
    # GET all published api
    text = Text.objects.filter(published=True)
        
    if request.method == 'GET': 
        text_serializer = TextSerializer(text, many=True)
        return JsonResponse(text_serializer.data, safe=False)