from django.contrib.auth import get_user_model
from django.db import models
UserModel = get_user_model()


class Design(models.Model):
    name = models.CharField(max_length=30)

    design_image = models.ImageField(
        upload_to='media/'
    )


class LikeDesign(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )