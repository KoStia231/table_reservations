from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Отображение главной страницы сайта"""
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AboutView(TemplateView):
    """Отображение главной страницы сайта"""
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
