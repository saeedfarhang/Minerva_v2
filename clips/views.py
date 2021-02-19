from .models import Clip
from .serializers import ClipSerializer
from rest_framework.views import APIView
from functions import *
from api_responses import *
from rest_framework.status import *
from rest_framework import permissions
from rest_framework.response import Response

class ClipsApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        data = request.data
        try:
            clips = Clip.objects.filter(is_published=True)
        except :
            return Response(item_not_found, HTTP_404_NOT_FOUND)
        serializer = ClipSerializer(clips, many=True)
        return Response(serializer.data, HTTP_200_OK)
    def post(self, request):
        data = request.data
        user = request.user
        if 'author' in data or 'date_added' in data:
            return Response(change_protected_fields, HTTP_400_BAD_REQUEST)
        tagname_to_tagid(data, data['tags'])
        data.update({'author':user.id})
        if user.is_qualify:
            serializer = ClipSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, HTTP_200_OK)
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
        return Response(not_have_access, HTTP_400_BAD_REQUEST)    
class ClipDetailApiView(APIView):
    def get(self,request, id, action):
        user = request.user
        try:
            clip = Clip.objects.get(id = id)
            if clip.is_published == False and clip.author != user:
                return Response(not_have_access, HTTP_400_BAD_REQUEST)
        except :
            return Response(item_not_found, HTTP_404_NOT_FOUND)
        if action == 'get':
            serializer = ClipSerializer(clip)
            return Response(serializer.data)

        elif action == 'delete':
            if clip.author == user:
                clip.delete()
                return Response(item_delete, HTTP_200_OK)
            return Response(not_have_access, HTTP_400_BAD_REQUEST)
        else:
            return Response(action_not_valid, HTTP_400_BAD_REQUEST)
        
    def post(self, request, id, action):
        data = request.data
        user = request.user
        try:
            clip = Clip.objects.get(id = id)
            if clip.is_published == False and clip.author != user:
                return Response(not_have_access, HTTP_400_BAD_REQUEST)
        except :
            return Response(unkown_error, HTTP_500_INTERNAL_SERVER_ERROR)
        if action == 'edit':
            if 'author' in data or 'date_added' in data:
                return Response(change_protected_fields, HTTP_400_BAD_REQUEST)
            data.update({'author':user.id})
            serializer = ClipSerializer(clip, data=data)
            if serializer.is_valid():
                return Response(serializer.data, HTTP_200_OK)
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)
        else:
            return Response(action_not_valid, HTTP_400_BAD_REQUEST)