from django.conf.urls import include, url
from .views import AuthRegister, PostList, LikeList,UserList
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^login/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
    url(r'^register/$', AuthRegister.as_view()),
    url(r'^posts/$', PostList.as_view()),
    # URL Created for manual login logic
    # url(r'^login/$', AuthLogin.as_view()),
    #api/like/?postid=2&like=false unlikes the post with an id of 2, set like to true to like the post
    url(r'^like/', LikeList.as_view()),
    url(r'^users/', UserList.as_view()) #gets userlist
]
