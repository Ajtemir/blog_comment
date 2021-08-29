from django.urls import path, include
from rest_framework import routers

from apis import views

router =routers.SimpleRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('article', views.ArticleViewSet.as_view())
]