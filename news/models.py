from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def update_rating(self):
        post_rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comment_rating = self.comment_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comment_rating_to_posts = self.post_set.aggregate(models.Sum('comments__rating'))['comments__rating__sum'] or 0

        self.rating = post_rating * 3 + comment_rating + comment_rating_to_posts
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type_choices = [
        ('article', 'Статья'),
        ('news', 'Новость')
    ]
    post_type = models.CharField(max_length=10, choices=post_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    content = models.TextField()  # Ранее было названо `post.content`
    rating = models.IntegerField(default=0)

    def preview(self):
        preview_length = 124
        if len(self.content) <= preview_length:
            return self.content
        else:
            return self.content[:preview_length] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comments')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()