from django.contrib import admin
from django.urls import path
from .quiz.views import RandomQuestion, CreateQuestionsView, QuestionAndAnswerView, QuestionDetailView
from .score.views import UpdateScores, Leaderboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # Fetch random question
    path('api/random/', RandomQuestion.as_view(), name='random'),

    # Update scores and leaderboard
    path('api/score/update/', UpdateScores.as_view(), name='score_update'),
    path('api/score/leaderboard/', Leaderboard.as_view(), name='leaderboard'),

    # Create questions
    path('api/questions/create/', CreateQuestionsView.as_view(), name='create-question'),

    # Get list of questions with answers
    path('api/questions/', QuestionAndAnswerView.as_view(), name='question-and-answer'),

    # Get, Update, or Delete a specific question by question_id (UUID)
    path('api/questions/<uuid:question_id>/', QuestionDetailView.as_view(), name='question-detail'),
]