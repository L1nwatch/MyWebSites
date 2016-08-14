#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
负责编写视图的地方
"""
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List

__author__ = '__L1n__w@tch'


# Create your views here.
def home_page(request):
    return render(request, "home.html")


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == "POST":
        try:
            # 注意这里不是 Item.objects.create()
            item = Item(text=request.POST["item_text"], list_attr=list_)
            item.full_clean()
            item.save()
            return redirect("/lists/{}/".format(list_.id))
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, "list.html", {"list_attr": list_, "error": error})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list_attr=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})
    return redirect("/lists/{unique_url}/".format(unique_url=list_.id))


if __name__ == "__main__":
    pass
