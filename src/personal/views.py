from django.shortcuts import render
from account.models import Account
from operator import attrgetter
from blog.models import BlogPost

# Create your views here.

# Funkcja odpowiadająca za wyświetlanie strony głównej (widok dla strony głównej)
def home_screen_view(request):

	context = {}
	blog_posts = sorted(BlogPost.objects.all(), key=attrgetter('date_updated'), reverse=True)
	context['blog_posts'] = blog_posts

	return render(request, "personal/home.html", context)

# Funkcja odpowiadająca za wyświetlanie 'O nas' ('O nas') 
def about_view(request):

	context = {}
	accounts = Account.objects.all()
	context['accounts'] = accounts

	return render(request, "personal/about.html", context)