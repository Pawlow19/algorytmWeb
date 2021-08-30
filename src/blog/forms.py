from django import forms

from blog.models import BlogPost 

# Klasa obsługująca formularz tworzenia postów
class CreateBlogPostForm(forms.ModelForm):
	# Meta klasa zarządzająca modelem
	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

# Klasa obsługująca formularz edycji postów
class UpdateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

	def save(self, commit=True):
		blog_post = self.instance
		blog_post.title = self.cleaned_data['title']
		blog_post.body = self.cleaned_data['body']

		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']

		if commit:
			blog_post.save()
		return blog_post