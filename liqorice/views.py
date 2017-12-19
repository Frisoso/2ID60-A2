from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from .models import Comment
from .serializers import CommentSerializer
from .forms import CommentForm

# Create your views here.
class HomePage(APIView):
    def get(self, request, format=None):
        comments = Comment.objects.filter(
            post_date__lte=timezone.now()
        ).order_by('post_date')
        form = CommentForm()
        return render(request, 'liqorice/liqorice_home.html', {'comments': comments, 'form': form})

    @method_decorator(permission_required('liqorice.add_comment'))
    def post(self, request, format=None):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.post_date = timezone.now()
            comment.save()
            return redirect('/#' + comment.id)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentNew(APIView):
    def get(self, request, format=None):
        form = CommentForm()
        return render(request, 'liqorice/comment_edit.html', {'form': form})

    @method_decorator(permission_required('liqorice.add_comment'))
    def post(self, request, format=None):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_date = timezone.now()
            comment.save()
            return redirect('liqorice_home')

class CommentList(APIView):
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @method_decorator(permission_required('liqorice.add_comment'))
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required('liqorice.delete_comment'))
    def delete(self, request, format=None):
        Comment.objects.all().delete();
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentDetail(APIView):
    def get(self, request, id, format=None):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @method_decorator(permission_required('liqorice.delete_comment'))
    def delete(self, request, id, format=None):
        comment = get_object_or_404(Comment, id=id)
        if comment.count() > 0:
            comment.delete();
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
