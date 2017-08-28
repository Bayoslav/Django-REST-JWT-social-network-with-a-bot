import json
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth import login, authenticate
from pyhunter import PyHunter
from .serializers import UserSerializer, PostSerializer
from .models import User, Post
import clearbit
User
class AuthRegister(APIView):
    """
    Register a new user.
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        clearbit.key = 'sk_a58ce3ff299332066447fe9eba0f0543'
        hunterAPI = '5aa57f6c3b4600d3a881a0d2b38e9311e5b91640'
        email = request.data.get('email')
        hunter = PyHunter(hunterAPI)
        verify_email = hunter.email_verifier(email)         #Checks if the email is deliverable or not  through hunterAPI
        if(verify_email.get('result')=='undeliverable'):
            return Response({'status': 'Incorrect data',
            'message': 'E-mail not deliverable'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            #enrichjson = 'blank'
            if not request.data._mutable:
                request.data._mutable = True
            #lookup = clearbit.Enrichment.find(email=email, stream=True)
            #if lookup != None:
              #enrichjson = (json.dumps(lookup['person'], sort_keys=True, indent=4))
             # print(enrichjson)
            serializer = self.serializer_class(data=request.data)
            #request.data['enrich_json'] = enrichjson
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthLogin(APIView):
    ''' Manual implementation of login method '''
    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        #email = data.get('email', None)
        password = data.get('password', None)

        User = authenticate(username=username, password=password)
        # Generate token and add it to the response object
        if User is not None:
            login(request, User)
            return Response({
                'status': 'Successful',
                'message': 'You have successfully been logged into your account.'
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'Unauthorized',
            'message': 'Username/password combination invalid.'
        }, status=status.HTTP_401_UNAUTHORIZED)

class PostList(APIView):
    #lists posts
    def get(self,request, format=None):
        Posts = Post.objects.all()
        serializer = PostSerializer(Posts, many=True, context={'request': request})
        return Response(serializer.data)
    def post(self,request, format=None):
        #creates a post
        jwt_token = (request.META.get('HTTP_AUTHORIZATION')) #Gets the token #JWT Ne radi dobro.
        print(request.user) #ne loguje ga dobro
        userid = request.user.id
        if not request.data._mutable:
            request.data._mutable = True
      # request.data.creator = username
       # serializer.data.creator = username does not work
        serializer = PostSerializer(data=request.data) #assigning value directly to the
        request.data['creator'] = userid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeList(APIView):
    serializer_class = PostSerializer
    #Post = Post.objects.all()
    def get(self,request,format=None):
        post_id = (int(request.GET.get('postid')))
        like = (request.GET.get('like'))
        userid = request.user.id
        Posts = get_object_or_404(Post, id=post_id)
        #print("Like is ", like) # testing purposes
        #print("PostID is ", post_id)
        #print("USER IS ", userid)
        if(like != 'false'):
            Posts.likers.add(userid) #adds the like to the db
        elif(like == 'false'):
            Posts.likers.remove(userid) #removes the like aka unlike
        serializer = PostSerializer(data=Posts)
        if serializer.is_valid():
            serializer.save() #saves it
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserList(APIView):
    serializer_class = UserSerializer
    def get(self,request, format=None):
        username = request.GET.get('username')
        if(username!=None):
            Users=get_object_or_404(User,username=username)
            serializer = UserSerializer(Users,many=False, context={'request': request})
        else:
            Users = User.objects.all()
            serializer = UserSerializer(Users, many=True, context={'request': request})
        return Response(serializer.data)
