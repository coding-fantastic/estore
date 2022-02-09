from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, "store/index.html")


def collections(request):
    category = Category.objects.filter(status=0)
    context = {"category": category}
    return render(request, "store/collections.html", context)


def collectionsview(request, slug):
    if Category.objects.filter(slug=slug, status=0):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {"products": products, "category": category}
        return render(request, "store/products/index.html", context)
    else:
        messages.warning(request, "No such category found ")
        return redirect("collections")


def productview(request, cate_slug, prod_slug):
    if Category.objects.filter(slug=cate_slug, status=0):
        # check if products is there
        if Product.objects.filter(slug=prod_slug, status=0):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            context = {"products": products}

        else:
            messages.error(request, "No such category found")
            return redirect("collections")
    else:
        messages.error(request, "No such category found")
        return redirect("collections")

    return render(request, "store/products/view.html", context)


def productlistAjax(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productList = list(products)
    return JsonResponse(productList, safe=False)
