from django.http import HttpResponseForbidden


class CanUpdateProductMixin:
    def dispatch(self, request, *args, **kwargs):
        product = self.object
        user = request.user
        if user.has_perm('shopapp.change_product') or product.created_by.user == user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('У вас недостаточно прав')