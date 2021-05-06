from SmartDjango import models


class Collocation(models.Model):
    word = models.CharField(
        max_length=20,
    )

    collocation = models.TextField()
