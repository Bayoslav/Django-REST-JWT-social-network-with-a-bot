from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers
from datetime import datetime
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'password','enrichjson')
        #read_only_fields = ('date_created', 'date_modified')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        #instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username',
                                               instance.username)

        password = validated_data.get('password', None)

        if password and password == confirm_password:
            instance.set_password(password)

        instance.save()
        return instance

    def validate(self, data):
        return data


class PostSerializer(serializers.ModelSerializer):
    #creator = serializers.PrimaryKeyRelatedField()
    date = serializers.DateTimeField(default=datetime.now())
    likers = serializers.PrimaryKeyRelatedField(
        many=True,queryset=Post.objects.all())
    class Meta:
        model = Post
        fields = ('creator','title','text','date','likers','id')

        ##def create(self, validated_data):
       #     validated_data['creator'] = self.context['request'].user

        #    return super(self, PostSerializer).create(validated_data)
'''class LikeSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(default=datetime.now())

    class Meta:
        model = Like
        fields=('user','post','date')'''
