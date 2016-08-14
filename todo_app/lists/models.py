from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])


# Create your models here.
class Item(models.Model):
    text = models.TextField(default="", blank=False)
    list_attr = models.ForeignKey(List, default=None)  # List 的声明得在该类上方
