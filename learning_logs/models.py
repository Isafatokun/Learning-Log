from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """Topics someone is studying"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Entry(models.Model):
    """Entries for the topics"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Special Class to return plural of Entry"""
        verbose_name_plural = 'entries'

    def __str__(self):
        """Returns a summary of the entry"""
        if len(self.text) > 50:
            pre = f"{self.text[:50]}..."
        else:
            pre = self.text
        return pre, self.title
