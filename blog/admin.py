from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Article, Comment

admin.site.register(Comment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_show', 'user', 'description', 'created', 'uploaded']
    list_filter = ['created', 'uploaded']

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return "None"

    image_show.__name__ = "Картинка"
