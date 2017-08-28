from django.conf.urls import url,include
from .views import PostList, UserList,LikeList
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token,verify_jwt_token

urlpatterns = [
    #url(r'^posts/', include(urls)),
    url(r'^api$', PostList.as_view()),
    url(r'^api/users/$', UserList.as_view()), #register
    url(r'api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    #(r'^posts/', include(urls)),
    url(r'^api-token-refresh/', refresh_jwt_token),
   #url(r'api-token-refresh/', refresh_jwt_token),
    url(r'^like/(?P<pk>[0-9]+)/$', LikeList.as_view(), name='likerestapi'),
]
format_suffix_patterns(urlpatterns)
