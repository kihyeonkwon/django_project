from django.urls import path
from community import views

app_name = 'community'

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:article_id>/", views.article_detail, name="article_detail"),
    path("create_article/", views.create_article, name="create_article"),
    path("update_article/<int:article_id>/", views.update_article, name="update_article"),
    path("delete_article/<int:article_id>/", views.delete_article, name="delete_article"),
    path("<int:article_id>/create_comment/", views.create_comment, name="create_comment"),
    path("<int:article_id>/delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),
]
