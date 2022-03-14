from django.contrib.auth.mixins import AccessMixin

class RoleRequiredMixin(AccessMixin):
    user_role_required = [20,10] 
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.role in self.user_role_required):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
