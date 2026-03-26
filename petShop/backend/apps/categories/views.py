from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Category
# Create your views here.

def categories(request, pk = None):
    if pk:
        parent = get_object_or_404(Category, pk=pk)
        categories = parent.get_children()
    else:
        parent = None
        categories = Category.objects.root_nodes()
    return render(request, 'categories.html', {"categories": categories, "parent": parent})