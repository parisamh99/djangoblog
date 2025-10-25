from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from blog.models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import mixins
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination


# create with api view in function
"""@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly,])
def postlist(request):
    if request.method == 'GET':
      posts = Post.objects.filter(status=True)
      serializers = PostSerializer(posts, many=True)
      return Response(serializers.data)
    elif request.method == 'POST':
       serializers = PostSerializer(data=request.data)
       if serializers.is_valid():
          serializers.save()
          return Response(serializers.data)
       else:
          return Response(serializers.errors)
"""

# create with APIVIEW CLASS
'''
class PostList(APIView):
   """getting a list of post and creating a new post"""
   permission_classes = [IsAuthenticated]
   serializer_class = PostSerializer
   def get(self,request):
      """retriveing a list of posts"""
      posts = Post.objects.filter(status=True)
      serializers = PostSerializer(posts, many=True)
      return Response(serializers.data)

   def post(self,request):
      """creating a post with provided data"""
      serializers = PostSerializer(data=request.data)
      if serializers.is_valid():
          serializers.save()
          return Response(serializers.data)
      else:
          return Response(serializers.errors)
'''


# CREATE WITH apiview in function
"""
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly,])
def postdetail(request,id):
    post = get_object_or_404(Post,pk=id, status=True)
    if request.method == 'GET':
      serializer = PostSerializer(post)
      return Response(serializer.data)
    elif request.method == 'PUT':
       serializer = PostSerializer(post, request.data)
       if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
       else:
          return Response(serializer.errors)
    elif request.method == 'DELETE':
       post.delete()
       return Response({'detail':'items deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
"""


class PostList(ListCreateAPIView):
    """getting a list of post and creating a new post"""

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)


'''
class PostDetail(APIView):
   """ getting detail of the post and edit plus removing it """
   permission_classes = [IsAuthenticatedOrReadOnly]
   serializer_class = PostSerializer
   def get(self,request,id):
      """ retriveing the post data """
      post = post = get_object_or_404(Post,pk=id, status=True)
      serializer =self.serializer_class(post)
      return Response(serializer.data)
   
   def put(self,request,id):
      """ editing the post data """
      post = post = get_object_or_404(Post,pk=id, status=True)
      serializer = self.serializer_class(post, request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
      else:
          return Response(serializer.errors)

   def delete(self,request,id):
      """ deleting the post object """
      post = post = get_object_or_404(Post,pk=id, status=True)
      post.delete()
      return Response({'detail':'items deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
'''


class PostDetail(RetrieveUpdateDestroyAPIView):
    """getting detail of the post and edit plus removing it"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)


# example for class_based_views
class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "category": ["exact", "in"],
        "author": ["exact", "in"],
        "status": ["exact", "in"],
    }
    search_fields = ["title", "content"]
    ordering_fields = ["published_date"]
    pagination_class = DefaultPagination


# these are for viewset
# def list(self,request):
#    serializer = self.serializer_class(self.queryset, many=True)
#    return Response(serializer.data)

# def retrieve(self,request,pk=None):
#    post_object = get_object_or_404(self.queryset,pk=pk)
#    serializer = self.serializer_class(post_object)
#    return Response(serializer.data)

# def create(self, request):
#    pass

# def destroy(self,request,pk=None):
#    pass

# def update(self,request,pk=None):
#    pass

# def partial_update(self,request,pk=None):
#    pass


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
