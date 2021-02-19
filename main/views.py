from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import permissions
from .models import Tag, Category
from courses.models import Course
from courses.serializers import CourseSerializer
from .serializers import CategorySerializer,TagSerializer

class CategoriesApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,request):
        query = Category.objects.all().order_by('title')
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data, HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        user = request.user
        if user.is_superuser:
            title = data['title']
            if Category.objects.filter(title = title).exists():
                return Response({'error':'this category already exists.'})
            
            data.update({"users":[1]})
            serializer = CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, HTTP_200_OK)
            else:
                return Response(serializer.errors, HTTP_404_NOT_FOUND)
        else:
            return Response({"error":'you can not preform this action'}, HTTP_404_NOT_FOUND)


class CategoryDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,request, id, action):
        if action == 'delete':
            if request.user.is_superuser:
                try:
                    category = Category.objects.get(id = id)
                    category.delete()
                    return Response({"success":"category with given id been deleted."}, HTTP_200_OK)
                except :
                    return Response({"error":"there is no category with the given id"}, HTTP_404_NOT_FOUND)
            else:
                return Response({"error":"you dont have access to do this action"}, HTTP_400_BAD_REQUEST)

        elif action == 'get':
            try:
                category = Category.objects.get(id = id)
                courses = Course.objects.filter(category=category)
                category_serializer = CategorySerializer(category)
                course_serializer = CourseSerializer(courses, many=True)

                return Response({"category":category_serializer.data,"courses":course_serializer.data}, HTTP_200_OK)
            except :
                return Response({"error":"there is no category with the given id"}, HTTP_404_NOT_FOUND)
        else:
            return Response({"error":"this action is unvalid"}, HTTP_400_BAD_REQUEST)
    

class TagsApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        query = Tag.objects.all().order_by('title')
        serializer = TagSerializer(query, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def post(self, request):
        data = request.data
        user = request.user
        if user.is_superuser:
            title = data['title']
            if Tag.objects.filter(title = title).exists():
                return Response({'error':'this tag already exists.'})
            
            data.update({"users":[1]})
            serializer = TagSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, HTTP_200_OK)
            else:
                return Response(serializer.errors, HTTP_404_NOT_FOUND)
        else:
            return Response({"error":'you can not preform this action'}, HTTP_404_NOT_FOUND)

class TagDetailApiView(APIView):
    def get(self, request, id):
        tag = Tag.objects.get(id = id)
        courses = Course.objects.filter(tags=tag)

        tag_serializer = TagSerializer(tag)
        course_serializer = CourseSerializer(courses, many=True)
        return Response({"tag":tag_serializer.data,"courses":course_serializer.data}, HTTP_200_OK)
