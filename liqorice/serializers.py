from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):

    id = serializers.CharField(required=False)
    author = serializers.CharField(required=False)
    owner = serializers.ReadOnlyField(source='owner.username', required=False)

    class Meta:
        model = Comment

        fields = ('id','author','post_date','content','owner')

class UserSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'comments')
