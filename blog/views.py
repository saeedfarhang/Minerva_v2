from django.shortcuts import render
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.status import *
from api_responses import *
from main.models import Tag, Category
from functions import *

class BlogApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        blogs = Blog.objects.filter(is_published = True)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        user = request.user
        if 'author' in data or 'date_added' in data or 'date_updated' in data:
            return Response(not_have_access,HTTP_400_BAD_REQUEST)
        if user.is_qualify:
            tag_list = []
            for tag in data["tags"]:
                try:
                    tag_item = Tag.objects.get(title=tag)
                    
                except :
                    Tag.objects.create(title=tag).save()
                    tag_item = Tag.objects.get(title=tag)                    
                tag_list.append(tag_item.id)
            data.update({'tags':tag_list})
            data.update({'author' : user.id})
            serializer = BlogSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,HTTP_200_OK)
            else:
                return Response(serializer.errors, HTTP_400_BAD_REQUEST)

class BlogDetailApiView(APIView):
    def get(self, request, id, action):
        user = request.user
        try:
            blog = Blog.objects.get(id = id)
            if blog.is_published == False:
                if blog.author == user.id:
                    pass
                else:
                    return Response(not_have_access, HTTP_400_BAD_REQUEST)
        except :
            return Response(item_not_found, HTTP_404_NOT_FOUND)
        if action == 'get':
            serializer = BlogSerializer(blog)
            return Response(serializer.data)
        
        elif action == 'delete':
            if blog.author == user:
                try:
                    blog.delete()
                    return Response(item_delete, HTTP_200_OK)
                except:
                    return Response(unkown_error, HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(not_have_access, HTTP_400_BAD_REQUEST)
        else:
            return Response(action_not_valid, HTTP_400_BAD_REQUEST)

    def post(self, request, id, action):
        data = request.data
        user = request.user
        if 'author' in data or 'date_added' in data or 'date_updated' in data:
            return Response(not_have_access,HTTP_400_BAD_REQUEST)
        try:
            blog = Blog.objects.get(id = id)
        except :
            return Response(item_not_found, HTTP_404_NOT_FOUND)
        if action == 'edit':
            if blog.author == user:
                data.update({'author':user.id})
                tagname_to_tagid(data, data['tags'])
                data.update({'date_updated':tehran_now()})
                serializer = BlogSerializer(blog, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)
