from django.urls import include, path
from rest_framework import routers

from .views import APISignup, GetTokenView

router = routers.DefaultRouter()

urlpatterns = [
    # path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view()),
    path('v1/auth/token/', GetTokenView.as_view(), name='token'),
]
