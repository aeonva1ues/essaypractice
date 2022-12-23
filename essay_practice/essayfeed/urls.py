from django.urls import path

from essayfeed.views import (DeleteEssayView, DeleteReportView,
                             EssayDetailView, EssayListView,
                             ModerationReportsView, MyEssaysListView,
                             DeleteCommentView, DeleteCommentReportView,
                             SendingCommentReportView)

app_name = 'essayfeed'

urlpatterns = [
    path('', EssayListView.as_view(), name='feed'),
    path('essay/<int:pk>/', EssayDetailView.as_view(), name='detail_essay'),
    path('sending_comment_report/',
         SendingCommentReportView.as_view(),
         name='post-comment_report'),
    path('my-essays/', MyEssaysListView.as_view(), name='my_essays'),
    path(
        'check-reports/',
        ModerationReportsView.as_view(), name='check-reports'),
    path(
        'essay/delete/<int:pk>',
        DeleteEssayView.as_view(), name='delete-essay'
    ),
    path(
        'report/delete/<int:pk>',
        DeleteReportView.as_view(), name='delete-report'
        ),
    path(
        'comment_report/delete/<int:pk>',
        DeleteCommentReportView.as_view(), name='delete-comment_report'
        ),
    path(
        'comment/delete/<int:pk>',
        DeleteCommentView.as_view(), name='delete-comment'
        )
]
