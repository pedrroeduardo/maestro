from django.contrib.auth.views import LoginView

from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_form(self, form_class=None):
        if self.request.method == "GET":
            return None
        return super().get_form(form_class)

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, "Username or password is incorrect.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login - Maestro'
        return context

login_view = CustomLoginView.as_view()
