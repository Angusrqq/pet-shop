from .models import Wishlist

def wishlist(request):
    if request.user.is_authenticated:
        ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    elif request.session.session_key:
        ids = Wishlist.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
    else:
        ids = []
    return {'wishlist_products': list(ids)}
