from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()



""" Note model """
class Note(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.title
    
    
