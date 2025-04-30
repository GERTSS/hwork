from django.http import HttpResponseForbidden


class CanUpdateUserMixin:
    def dispatch(self, request, *args, **kwargs):
        profile = self.object
        user = request.user
        if user.has_perm('myauth.change_profile') or profile.user == user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('У вас недостаточно прав')