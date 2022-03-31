from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView


# @method_decorator(cache_page(60 * 10), name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home_2.html'


# @method_decorator(cache_page(60 * 10), name='dispatch')
class CauseView(TemplateView):
    template_name = 'cause.html'


def handler404(request, exception):
    return render(request, 'error_404.html', status=404)


def handler500(request):
    return render(request, 'error_500.html', status=500)
