def categories_processor(request):
    from .models import Category
    return {
        'all_categories': Category.objects.all().order_by('name')
    }
