from django.db import models

from accounts.models import *

# Create your models here.

class Thread(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def subscribers(self):
        """Return all users subscribed to this thread."""
        return User.objects.filter(thread_subscriptions__thread=self)


class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.thread}"


class ThreadSubscription(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='subscriptions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_subscriptions')
    subscription = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('thread', 'user')

    def __str__(self):
        return f"{self.user} subscribed to {self.thread}"