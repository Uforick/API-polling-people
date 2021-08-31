from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AnswerForChoiceViewSet, PollDetailPageViewSet, PollViewSet,
                    QuestionViewSet, UserChoiceAnswerVievSet,
                    choice_answer_view)

router_v1 = DefaultRouter()

router_v1.register(
    r'poll',
    PollViewSet,
    'poll',
)

router_v1.register(
    r'poll',
    PollDetailPageViewSet,
    'poll',
)

router_v1.register(
    r'poll/(?P<poll_id>[\d]+)/question',
    QuestionViewSet,
    'question',
)

router_v1.register(
    r'poll/(?P<poll_id>[\d]+)/question/(?P<question_id>[\d]+)/answers',
    AnswerForChoiceViewSet,
    'answers',
)

router_v1.register(
    r'my_answers',
    UserChoiceAnswerVievSet,
    'choice-answer',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/poll/<int:poll_id>/question/<int:question_id>/choice-answer/',
        choice_answer_view,
        name='choice-answer',
    ),
]
