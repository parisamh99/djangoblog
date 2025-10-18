from django.urls import path, include
from . import views
from django.views.generic import TemplateView, RedirectView


app_name = 'blog'

urlpatterns =[
    #path('fbv-index/', views.indexView, name='fbv_index'),
    #path('cbv-index/', TemplateView.as_view(template_name = 'blog/index.html', extra_context = {'name':'paisa'},)),
    path('cbv-index/', views.IndexView.as_view(), name='cbv_index'),
    path('go-to-maktab/<int:pk>', views.Redirecttomaktab.as_view(), name='go-to-maktab'),
    path('post/',views.PostListView.as_view(), name='post-list'),
    path('detail/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('api/v1/', include('blog.api.v1.urls')),
] 