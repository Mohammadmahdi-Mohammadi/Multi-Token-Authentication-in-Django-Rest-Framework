
from django.contrib import admin
from django.urls import path,include

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# from posts.views import RevokeToken
from posts.views import RegisterUserAPIView,Logout,livetoken

router = DefaultRouter()
# router.register("", UserHandler, basename="Users")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('register/', RegisterUserAPIView.as_view()),


    path('get_token/', obtain_auth_token),
    # path('revoke_token/', RevokeToken.as_view() ),

    path('Logout/', Logout.as_view()),
    path('Live_token/', livetoken.as_view({'get': 'list'}))

    # url(r'^logout/', Logout.as_view()),


    # path('')
    # to get recently token
    # path()
    # path(Revoke)

    # path('user/', include(router)),
    # path('index/<int:pk>/', index) ,  # index dosent need ()
    # path('index/', index),  # index dosent need ()
    # path('posts/' , post_list, name = 'post-list'),
    # # path('posts/<int:post_id>/', post_detail, name= 'post-detail'),
    # path('posts/create/', post_create),
    # path('posts/<int:pk>/', PostDetail.as_view()),
]

