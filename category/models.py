from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["category_name"]

    def __str__(self):
        return self.category_name
