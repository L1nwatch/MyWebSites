from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="lists_want_to_share")

    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list_attr=list_)
        return list_

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
