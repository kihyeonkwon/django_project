from django.http import HttpResponse
from django.shortcuts import redirect, render
from community.models import Article, Comment
from django.db.models import Count

# Create your views here.

def index(request):
    # articles = Article.objects.all().order_by('-created_at')
    articles = Article.objects.annotate(num_comment=Count('comment')).order_by('-created_at')
    context = {
        'articles':articles
    }
    return render(request, 'index.html', context)


def create_article(request):
    if request.method == 'GET':
        return render(request, 'create_article.html')
    elif request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        Article.objects.create(title=title, content=content, user=request.user)
        return redirect('community:index')

def article_detail(request, article_id):
    #getobject or 404로 치환
    article = Article.objects.get(pk=article_id)
    context = {
        'article':article
    }
    return render(request, 'article_detail.html', context)

def update_article(request, article_id):
    if request.method == 'GET':
        article = Article.objects.get(pk=article_id)
        context={
            'article':article
        }
        return render(request, 'update_article.html', context)
    elif request.method == 'POST':
        article = Article.objects.get(pk=article_id)
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.save()
        return redirect('community:article_detail', article_id)


def delete_article(request, article_id):
    if request.method == 'POST':
        article = Article.objects.get(pk=article_id)
        article.delete()
        return redirect('community:index')

def create_comment(request, article_id):
    if request.method == 'POST':
        Comment.objects.create(content= request.POST.get("content"), user = request.user, article_id=article_id)
        return redirect('community:article_detail', article_id)

def delete_comment(request, article_id, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_id)
        if request.user == comment.user:
            comment.delete()
            return redirect('community:article_detail', article_id)
        else:
            return HttpResponse("not yours")