#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
负责编写视图的地方
"""
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import Item, List

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

__author__ = '__L1n__w@tch'

User = get_user_model()


# Create your views here.
def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            # Item.objects.create(text=request.POST["text"], list_attr=list_)
            return redirect(list_)
            # try:
            #     注意这里不是 Item.objects.create()
            # item = Item(text=request.POST["text"], list_attr=list_)
            # item.full_clean()
            # item.save()
            # return redirect(list_)
            # except ValidationError:
            #     error = "You can't have an empty list item"
    return render(request, "list.html", {"list_attr": list_, "form": form})


def new_list2(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, "home.html", {"form": form})


def new_list(request):
    # 把 request.POST 中的数据传给表单的构造方法
    form = ItemForm(data=request.POST)

    # 使用 form.is_valid() 判断提交是否成功
    if form.is_valid():
        # list_ = List.objects.create()
        list_ = List()
        list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        # Item.objects.create(text=request.POST["text"], list_attr=list_)
        return redirect(list_)
    else:
        # 如果提交失败，把表单对象传入模板，而不显示一个硬编码的错误消息字符串
        return render(request, "home.html", {"form": form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, "my_lists.html", {"owner": owner})


if __name__ == "__main__":
    pass
