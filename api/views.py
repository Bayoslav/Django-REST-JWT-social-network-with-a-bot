from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
import jwt
from rest_framework_jwt.utils import jwt_payload_handler, jwt_get_user_id_from_payload_handler,jwt_decode_handler

class PostList(APIView):
    #lists posts
    def get(self,request, format=None):
        Posts = Post.objects.all()
        serializer = PostSerializer(Posts, many=True)
        return Response(serializer.data)
    def post(self,request, format=None):
        #creates a post
        jwt_token = (request.META.get('HTTP_AUTHORIZATION')) #Gets the token #JWT Ne radi dobro.
        print(request.user) #ne loguje ga dobro
        if not request.data._mutable:
            request.data._mutable = True
      # request.data.creator = username
       # serializer.data.creator = username does not work
        serializer = PostSerializer(data=request.data) #assigning value directly to the
        #request.data['creator'] = userid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):

    def get(self,request):
        #Lists users
        Users = User.objects.all()
        serializer = UserSerializer(Users, many=True)
        return Response(serializer.data)
    def post(self,request):
        #Registers a user
        print(request.user)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeList(APIView):
    def get(self,request):
        Likes = Like.objects.all()
        serializer = LikeSerializer(Likes, many=True)
        return Response(serializer.data)
    def post(self,request,p_id):
        userid = request.user.id
        if not request.data._mutable:
            request.data._mutable = True
        serializer = LikeSerializer(request.data)
        request.data['User'] = userid
        request.data['Post'] = p_id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
