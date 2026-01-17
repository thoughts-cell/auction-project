from .models import  Category
def categories_processor (request):
    return {
        'all-categories':Category.objects.all().order_by('name')
    }