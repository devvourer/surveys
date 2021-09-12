from django.urls import path

from .views import SurveyViewSet, QuestionViewSet, ChoiceViewSet, AnswerViewSet, login

# survey views
survey_list = SurveyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
survey_detail = SurveyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
# question views
question_view = QuestionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
question_create = QuestionViewSet.as_view({
    'post': 'create'
})
# choice views
choice_create = ChoiceViewSet.as_view({
    'post': 'create',
})
choice_view = ChoiceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
# answer views
answer_view = AnswerViewSet.as_view({
    'get': 'list',
})
answer_create = AnswerViewSet.as_view({
    'post': 'create',
})


urlpatterns = [
    path('surveys/', survey_list, name='survey_list'),
    path('surveys/<int:pk>/', survey_detail, name='survey_detail'),
    path('question/create/', question_create, name='question_create'),
    path('question/<int:pk>/', question_view, name='question_view'),
    path('choice/create/', choice_create, name='choice_create'),
    path('choice/<int:pk>/', choice_view, name='choice_view'),
    path('answers/create/', answer_create, name='answer_create'),
    path('answers/', answer_view, name='answer_view'),
    path('login/', login, name='login'),
]
