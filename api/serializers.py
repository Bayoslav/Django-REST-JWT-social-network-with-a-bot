from rest_framework import serializers
from .models import User, Post, Like
from datetime import datetime
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class PostSerializer(serializers.ModelSerializer):
    #creator = serializers.PrimaryKeyRelatedField()
    date = serializers.DateTimeField(default=datetime.now())
    class Meta:
        model = Post
        fields = ('creator','title','text','date')

        ##def create(self, validated_data):
       #     validated_data['creator'] = self.context['request'].user

        #    return super(self, PostSerializer).create(validated_data)
class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
