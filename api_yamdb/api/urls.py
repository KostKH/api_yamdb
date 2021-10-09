from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, CategoriesViewSet, TitlesViewSet, APISignup, GetTokenView

router_v1 = DefaultRouter()

router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('titles', TitlesViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignup.as_view()),
    path('v1/auth/token/', GetTokenView.as_view(), name='token'),
]
