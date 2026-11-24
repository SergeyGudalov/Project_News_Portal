from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating = 0

        # Сумма рейтингов статей автора
        for post in self.post_set.all():
            rating += post.rating

        rating *= 3

        # Сумма рейтингов комментариев автора
        for comment in Comment.objects.filter(user=self.user):
            rating += comment.rating

        # Сумма рейтингов под публикациями автора
        for comment in Comment.objects.filter(post__author=self):
            rating += comment.rating

        self.rating = rating
        self.save()

class Category(models.Model):
    name = models.CharField(unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    ARTICLE = "AR"
    NEWS = "NW"

    POST_TYPES = [
        (ARTICLE, "Статья"),
        (NEWS, "Новость"),
    ]
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE
                               )
    post_type = models.CharField(max_length=2,
                                 choices=POST_TYPES
                                 )
    created_at = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField(Category,
                                        through='PostCategory'
                                        )
    title = models.CharField(max_length=255)

    text = models.TextField()

    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + "..."




class PostCategory(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE
                             )
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE
                                 )


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE
                             )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE
                             )
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
