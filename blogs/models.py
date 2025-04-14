from django.db import models

# Create your models here.

class Blog(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_body = models.TextField()

    def __str__(self):
        return self.blog_title
    
class Comment(models.Model):
    # a blog can contain multiple comments
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')  # on_delete=models.CASCADE means if the blog got deleted, then comments should also get deleted.
    comment = models.TextField()

    def __str__(self):
        return self.comment