from django.urls import path
from . import views

urlpatterns = [
    # URL for the view to retrieve count of total favorite and read questions per user, paginated to 100 users per page
    path('user-question-count/', views.user_question_count_view, name='user_question_count'),

    # URL for the view to filter questions by read, unread, favorite, and unfavorite status
    path('filtered-questions/', views.filtered_question_view, name='filtered_questions'),

    # URL for the view to insert favorite question for a user
    path('add_favorite_question/', views.add_favorite_question, name='add_favorite_question'),

    # URL for the view to insert read question for a user
    path('add_read_question/', views.add_read_question, name='add_read_question'),

    # URL for the view to retrieve favorite and read questions for a user
    path('favorite_read_questions/<int:user_id>/', views.get_favorite_and_read_questions, name='favorite_read_questions'),
]
