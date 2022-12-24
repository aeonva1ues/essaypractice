from django.urls import path

from essayfeed.views import (DeleteEssayView, DeleteReportView,
                             EssayDetailView, EssayListView,
                             ModerationReportsView, MyEssaysListView,
                             DeleteCommentReportView, PostCommentReportView,
                             BanUserReportView)

app_name = 'essayfeed'

urlpatterns = [
    path('', EssayListView.as_view(), name='feed'),
    path('essay/<int:pk>/', EssayDetailView.as_view(), name='detail_essay'),
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
        'comment-report/send/',
        PostCommentReportView.as_view(), name='report-comment'
    ),
    path(
        'comment_report/ban-user/<int:pk>',
        BanUserReportView.as_view(), name='ban-user'
        ),
    path(
        'comment/delete/<int:pk>',
        DeleteCommentReportView.as_view(), name='delete-comment-report'
        )
]
