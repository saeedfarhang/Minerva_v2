from .models import Course, Lesson
from .serializers import CourseSerializer
from rest_framework.views import APIView
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import permissions
from datetime import datetime
import pytz
from main.models import Category, Tag

def tehran_now():
    tz = pytz.timezone('Asia/tehran')
    return datetime.now(tz)

class CourseApiView(APIView):
    # list all the courses
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        courses_query = Course.objects.filter(published = True).order_by('-date_added')
        serializer = CourseSerializer(courses_query, many=True)
        return Response(serializer.data, HTTP_200_OK)
    # create new course
    def post(self, request):
        user = request.user
        data = request.data
        if user.is_master:
            if 'selected' in data or 'master' in data or 'updated_date' in data:
                if user.is_superuser == False:
                    return Response({'error':'you can not change some of fields'}, HTTP_400_BAD_REQUEST)
            if 'tags' in data:
                tag_list = []
                for tag in data["tags"]:
                    try:
                        tag = Tag.objects.get(title = tag)
                        tag_list.append(tag.id)
                    except:
                        Tag.objects.create(title = tag).save()
                        tag = Tag.objects.get(title = tag)
                        tag_list.append(tag.id)
            
                data.update({'tags':tag_list})
            else:
                return Response({'error':'you must add at least 1 tag'})

            data.update({'master' : user.id})
            data.update({'updated_date' : tehran_now()})
            serializer = CourseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # print(tag.users.)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, HTTP_400_BAD_REQUEST)

        else:
            return Response({'error':'you are not allow to do this action.'}, HTTP_400_BAD_REQUEST)

class CourseDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, id, action):
        user = request.user
        if action == 'edit':
            return Response({'error':'this action doesnt allow on post method'}, HTTP_400_BAD_REQUEST)
        # see course detail
        elif action == 'get':
            try:
                course = Course.objects.get(id = id)
            except:
                return Response({'error':'there is no course with givin id'}, HTTP_404_NOT_FOUND)
            if course.published:
                serializer = CourseSerializer(course)
                return Response(serializer.data, HTTP_200_OK)
            return Response({'error':'you dont have access to see this course'}, HTTP_400_BAD_REQUEST)
        # delete course
        elif action == 'delete':
            try:
                course = Course.objects.get(id = id)
            except:
                return Response({'error':'there is no course with givin id'}, HTTP_404_NOT_FOUND)
            if course.master != user:
                return Response({'error':'only course master can delete it'},HTTP_400_BAD_REQUEST)
            course.delete()
            return Response({'success':f'course with id {id} been deleted.'}, HTTP_200_OK)
        else:
            return Response({'error':'unknow action'}, HTTP_400_BAD_REQUEST)    

    # edit course with id
    def post(self, request, id, action):
        if action == 'delete':
            return Response({'error':'this action doesnt allow on post method'}, HTTP_400_BAD_REQUEST)
        elif action == 'edit':
            user = request.user
            course = Course.objects.get(id = id)
            data = request.data
            if 'selected' in data or 'master' in data or 'updated_date' in data:
                if user.is_superuser == False:
                    return Response({'error':'you can not change some of fields'}, HTTP_400_BAD_REQUEST)
            if course.master != user:
                return Response({'error':'only course master can edit it'},HTTP_400_BAD_REQUEST)
            
            if 'tags' in data:
                tag_list = []
                for tag in data["tags"]:
                    try:
                        tag = Tag.objects.get(title = tag)
                        tag_list.append(tag.id)
                    except:
                        Tag.objects.create(title = tag).save()
                        tag = Tag.objects.get(title = tag)
                        tag_list.append(tag.id)
                        
                data.update({'tags':tag_list})
            else:
                return Response({'error':'you must add at least 1 tag'})

            data.update({'master' : user.id})
            data.update({'updated_date' : course.updated_date})
            serializer = CourseSerializer(course, data=data)
            if serializer.is_valid():
                serializer.save()

                if user in tag.users:
                    pass
                else:
                    tag.users.add(user)

                return Response(serializer.data, HTTP_200_OK)
            else:
                return Response(serializer.errors, HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'unknow action'}, HTTP_400_BAD_REQUEST)
            
class LessonsApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id = course_id)
        except :
            return Response({'error':f'there isnt any course with id {course_id}'}, HTTP_404_NOT_FOUND)

        lessons = Lesson.objects.filter(course = course).order_by('date_added')
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, HTTP_200_OK)


    def post(self, request, course_id):
        user = request.user
        data = request.data
        try:
            course = Course.objects.get(id = course_id)
        except :
            return Response({'error':f'there isnt any course with id {course_id}'}, HTTP_404_NOT_FOUND)
        
        if course.master != user:
            return Response({'error':'you dont have access to do this action'}, HTTP_400_BAD_REQUEST)

        if 'course' in data or 'master' in data:
            return Response({'error':'you can not change some of fields'}, HTTP_400_BAD_REQUEST)

        if 'tags' in data:
            tag_list = []
            for tag in data["tags"]:
                try:
                    tag = Tag.objects.get(title = tag)
                    tag_list.append(tag.id)
                except:
                    Tag.objects.create(title = tag).save()
                    tag = Tag.objects.get(title = tag)
                    tag_list.append(tag.id)

            data.update({'tags':tag_list})

        data.update({'master' : user.id})
        data.update({'course' : course.id})

        serializer = LessonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            Course.objects.filter(id = course_id).update(updated_date=tehran_now())
            return Response(serializer.data, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)

class LessonDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request ,course_id,lesson_id,action):
        user = request.user
        try:
            lesson = Lesson.objects.get(course=course_id, id=lesson_id)
        except:
            return Response({'error':f'can not get lesson {lesson_id} of course {course_id}'}, HTTP_404_NOT_FOUND)
        
        if action == 'get':
            serializer = LessonSerializer(lesson)
            return Response(serializer.data, HTTP_200_OK)
            
        elif action == 'delete':
            if lesson.master != user:
                return Response({'error':'you do not have access to delete this lesson'}, HTTP_400_BAD_REQUEST)
            try:
                lesson.delete()
                return Response({'success':'lesson been deleted'}, HTTP_200_OK)
            except :
                return Response({'error':'there is an error while i was try to delete this lesson. please try another time'}, HTTP_400_BAD_REQUEST)

        else:
            return Response({'error':f'{action} is an unknown action. choose between get or delete'}, HTTP_400_BAD_REQUEST)

    def post(self, request,course_id,lesson_id,action):
        data = request.data
        user = request.user
       
        try:
            lesson = Lesson.objects.get(course=course_id, id=lesson_id)
        except :
            return Response({'error':f'can not get lesson {lesson_id} of course {course_id}'}, HTTP_404_NOT_FOUND)

        if lesson.master == user:
            if action == 'edit':
                if 'date_added' in data or 'course' in data or 'master' in data:
                    return Response({'error':'you can not edit date_added, course or master field'}, HTTP_400_BAD_REQUEST)
                if 'tags' in data:
                    tag_list = []
                    for tag in data["tags"]:
                        try:
                            tag = Tag.objects.get(title = tag)
                            tag_list.append(tag.id)
                        except:
                            Tag.objects.create(title = tag).save()
                            tag = Tag.objects.get(title = tag)
                            tag_list.append(tag.id)

                    data.update({'tags':tag_list})
                data.update({'master' : user.id})
                data.update({'course' : course_id})
                serializer = LessonSerializer(lesson, data=data)    
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, HTTP_200_OK)
                else:
                    return Response(serializer.errors, HTTP_400_BAD_REQUEST)     
            else:
                return Response({'error':f'{action} is an unknown action. choose edit'}, HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'only course master can do this action/ try get for action'}, HTTP_400_BAD_REQUEST)