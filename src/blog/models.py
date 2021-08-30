from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
# Create your models here.

# Funkcja odpowiadająca za przypisanie lokalizacji na serwerze plikowi obrazu dołączonemu do posta
def upload_location(instance, filename):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
				author_id=str(instance.author.id),title=str(instance.title), filename=filename)
	return file_path

# Klasa odpowiadająca za model postów
class BlogPost(models.Model):
	title				= models.CharField(max_length=50, null=False, blank=False)
	body				= models.TextField(max_length=5000, null=False, blank=False)
	image				= models.ImageField(upload_to=upload_location, null=False, blank=False)
	date_published		= models.DateTimeField(auto_now_add=True, verbose_name="data dodania")
	date_updated		= models.DateTimeField(auto_now_add=True, verbose_name="data modyfikacji")
	author				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug				= models.SlugField(blank=True, unique=True)

	# Metoda zwracająca tytuł posta
	def __str__(self):
		return self.title

# Funkcja usuwająca plik obrazu z serwera po usunięciu postu
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)

# Funkcja sprawdzająca adres dla posta przed jego zapisaniem do bazy danych
def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)