from django.forms import ModelForm
from apps.repositories.models import Repository

class RepositoryForm(ModelForm):

    class Meta:
        model = Repository
        fields = ['description', 'homepage',]



"""
# Creating a form to add an article.
form = ArticleForm()
# Creating a form to change an existing article.
>>> article = Article.objects.get(pk=1)
>>> form = ArticleForm(instance=article)
f = ArticleForm(request.POST, instance=a)
""" 
