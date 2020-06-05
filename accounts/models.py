from django.db import models


# Create your models here.
class UserInformation(models.Model):
    user_email = models.EmailField()
    user_id = models.IntegerField()
    user_name = models.TextField()

    def __str__(self):
        return self.user_name
