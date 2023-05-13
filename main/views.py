from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required

def index(request):
    return redirect('real_estate')
    # return render(request, 'main/index.html')
    
def policy(request):
    return render(request, 'main/policy.html')

def about(request):
    return render(request, 'main/about.html')

def handler404(request, exception):
    return render(request, 'main/404.html', status=404)
    
def page_404(request): # for debag mode test by enter www.site.com/404
    return render(request, 'main/404.html')