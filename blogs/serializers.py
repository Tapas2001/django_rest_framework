from rest_framework import serializers
from .models import Blog, Comment


# 1. Standard Serializer for Blog and Comment

# step-1
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# # step-2 (standard)(not shows any comments inside the blog data)
# class BlogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Blog
#         fields = '__all__'


# nested serializers(it shows all comments) 
# step-2
class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True) #here variable name comment is same as related_name='comments' on models module and many=True for many comments
    class Meta:
        model = Blog
        fields = '__all__' 