from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class Category(models.Model):
    title = models.CharField(max_length=100)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent',
                                  blank=True, null=True,default=None)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Article(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='articles',
                                 on_delete=models.CASCADE,
                                 )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=150, db_index=True)
    # image = models.ImageField(upload_to='images', default='no_image.jpg', blank=True)
    image = CloudinaryField('image')
    description = models.TextField(max_length=1000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)
    comments = GenericRelation('comment')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        index_together = ('id',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.id])


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский комментарий',
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, verbose_name='Дата создания комментария')
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_parent(self):
        if not self.parent:
            return ""
        return self.parent

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
