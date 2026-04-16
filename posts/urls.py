from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_post, name="create_post"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),

    # report actions
    path("posts/<int:post_id>/report/", views.report_post, name="report_post"),
    path("comments/<int:comment_id>/report/", views.report_comment, name="report_comment"),
    path("posts/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("comments/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("posts/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("comments/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path("moderation/", views.moderation_dashboard, name="moderation_dashboard"),
    path("moderation/posts/<int:post_id>/unreport/", views.unreport_post, name="unreport_post"),
    path("moderation/comments/<int:comment_id>/unreport/", views.unreport_comment, name="unreport_comment"),
]