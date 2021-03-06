from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator

from .models import Comment
from .serializers import CommentSerializer, UserSerializer
from .forms import CommentForm

# Create your views here.
class HomePage(APIView):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Comment.objects.none()

    def get(self, request, format=None):
        comments = Comment.objects.filter(
            post_date__lte=timezone.now()
        ).order_by('post_date')
        form = CommentForm()
        return render(request, 'liqorice/liqorice_home.html', {'comments': comments, 'form': form})

    def post(self, request, format=None):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.owner = request.user
            comment.post_date = timezone.now()
            comment.save()
            messages.success(request, 'Placed comment')
            return redirect('/#' + comment.id)
        messages.error(request, 'Error placing comment')
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentList(APIView):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Comment.objects.none()

    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        Comment.objects.all().delete();
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentDetail(APIView):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Comment.objects.none()

    def get(self, request, id, format=None):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, id, format=None):
        comment =  get_object_or_404(Comment, id=id)
        print(comment.owner)
        if comment.owner != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(APIView):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = User.objects.none()

    def get(self, request, id, format=None):
        if int(id) != request.user.id and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = get_object_or_404(User, id=id)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

def custom_login(request, *args, **kwargs):
    response = login(request, *args, **kwargs)
    if request.user.is_authenticated():
        messages.success(request, "Logged in")
    return response

def custom_logout(request, *args, **kwargs):
    response = logout(request, *args, **kwargs)
    if not request.user.is_authenticated():
        messages.success(request, "Logged out")
    return response
