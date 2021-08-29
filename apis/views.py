from rest_framework import viewsets
from rest_framework.decorators import api_view

from apis.serializers import CategorySerializer, ArticleSerializer
from blog.models import Category, Article

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
