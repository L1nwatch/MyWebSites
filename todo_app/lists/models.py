from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])

    @property
    def name(self):
        return self.item_set.first().text


# Create your models here.
class Item(models.Model):
    class Meta:
        ordering = ("id",)
        unique_together = ("text", "list_attr")

    text = models.TextField(default="", blank=False, unique=False)
    list_attr = models.ForeignKey(List, default=None)  # List 的声明得在该类上方

    def __str__(self):
        return self.text
