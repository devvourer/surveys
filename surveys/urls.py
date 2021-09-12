from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import SurveyViewSet, QuestionViewSet, ChoiceViewSet, AnswerViewSet, login


# api
schema_view = get_schema_view(
    openapi.Info(
        title='Surveys API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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

    # API
    path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
