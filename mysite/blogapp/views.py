from django.views.generic import ListView

from blogapp.models import Article


class ListArticleView(ListView):
    queryset = (Article.objects.select_related('author', 'category')
                .prefetch_related('tags')
                .defer('content', 'author__bio',))
    template_name = 'blogapp/list_articles.html'
    context_object_name = 'articles'
