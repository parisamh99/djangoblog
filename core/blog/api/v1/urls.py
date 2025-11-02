from django.urls import path, include
from . import views
from django.views.generic import TemplateView, RedirectView
from rest_framework.routers import DefaultRouter

app_name = "api-v1"

router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModelViewSet, basename="category")

urlpatterns = router.urls

# urlpatterns =[
#     #path('post/',views.postlist, name='post_list'),
#     #path('post/<int:id>/',views.postdetail,name='post_detail'),
#     # path('post/',views.PostList.as_view(), name='post_list'),
#     # path('post/<int:pk>/',views.PostDetail.as_view(),name='post_detail'),
#     path('post/', views.PostViewSet.as_view({'get':'list','post':'create'}),name='post_list'),
#     path('post/<int:pk>/', views.PostViewSet.as_view({'get':'retrieve','delete':'destroy','put':'update','patch':'partial_update'}),name='post_detail'),
# ]

