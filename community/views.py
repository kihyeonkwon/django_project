from django.http import HttpResponse
from django.shortcuts import render, redirect
from community.models import Article, Comment
from django.shortcuts import get_object_or_404
from django.db.models import Count

# Create your views here.

def index(request):
    # articles = Article.objects.all().order_by('-created_at')
    articles = Article.objects.annotate(num_comments=Count('comment'))
    context={
        "articles":articles
    }

    return render(request, "index.html", context)


def create_article(request):
    if request.method == "GET":
        return render(request, "create_article.html")
    elif request.method == "POST":
        # input name=title 기훈님안녕하세요
        title = request.POST.get("title")
        # print(title) -> 기훈님안녕하세요
        content = request.POST.get("content")
        user = request.user
        Article.objects.create(title=title, content=content, user = user)
        return redirect("community:index")

def article_detail(request, article_id):
    if request.method == 'GET':
        article = Article.objects.get(id=article_id)
        # article = get_object_or_404(Article, id=article_id)
        context = {
            "article":article
        }
        return render(request, "article_detail.html", context)


def update_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.user != article.user:
        return HttpResponse("권한이 없습니다.")

    if request.method == 'GET':
        context = {
        "article":article
        }
        return render(request, "update_article.html", context)

    elif request.method == 'POST':
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.save()
        return redirect("community:article_detail", article_id)



def delete_article(request, article_id):
    if request.method == 'POST':
        article = Article.objects.get(id=article_id)
        if request.user != article.user:
            return HttpResponse("권한이 없습니다.")
        article.delete()
        return redirect("community:index")

def create_comment(request, article_id):
    if request.method == 'POST':
        content = request.POST.get("content")
        user = request.user
        Comment.objects.create(content=content, user = user, article_id= article_id)
        return redirect("community:article_detail", article_id)


def delete_comment(request, article_id, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return redirect("community:article_detail", article_id)
        else:
            return HttpResponse("권한이 없습니다!")