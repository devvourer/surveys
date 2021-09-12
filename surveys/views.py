from django.contrib.auth import authenticate
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token

from .serializers import SurveySerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer
from .models import Survey, Question, Choice, Answer
from .anonymous_user import Anonymous


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def list(self, request, *args, **kwargs):
        queryset = Survey.objects.filter(end_date__gte=timezone.now()).filter(pub_date__lte=timezone.now())
        serializer = SurveySerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if IsAdminUser().has_permission(request, self):
            return super().update(request)

    def destroy(self, request, *args, **kwargs):
        if IsAdminUser().has_permission(request, self):
            return super().destroy(request)

    def create(self, request, *args, **kwargs):
        if IsAdminUser().has_permission(request, self):
            serializer = SurveySerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                survey = serializer.save()
                return Response(SurveySerializer(survey).data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        survey = Survey.objects.get(id=instance.survey.id)
        if survey.pub_date is None:
            if IsAdminUser().has_permission(request, self):
                return super().update(request)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        survey = Survey.objects.get(id=instance.survey.id)
        if survey.pub_date is None:
            if IsAdminUser().has_permission(request, self):
                return super().destroy(request)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def create(self, request, *args, **kwargs):
        if IsAdminUser().has_permission(request, self):
            serializer = QuestionSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                survey = serializer.validated_data['survey']
                if survey.pub_date is None:
                    question = serializer.save()
                    return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def update(self, request, *args, **kwargs):
        if IsAdminUser().has_permission(request, self):
            return super().update()

    def destroy(self, request, *args, **kwargs):
        if IsAdminUser().has_permission(request, self):
            return super().destroy(request)

    def create(self, request, *args, **kwargs):
        if IsAdminUser().has_permission(request, self):
            serializer = ChoiceSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                choice = serializer.save()
                return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def list(self, request):
        if request.user.id is not None:
            answers = Answer.objects.filter(user_id=request.user.id)
        else:
            anonym_user = Anonymous(request)
            print(anonym_user.__dict__)
            answers = Answer.objects.filter(user_id=anonym_user.anonym_user['id'])

        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.id is None:
            # anonym_user = Anonymous(request)
            serializer = AnswerSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                # print(serializer.validated_data)
                # answer_id = serializer.validated_data['id']
                # anonym_user.add_answers(answer_id)
                answer = serializer.save()
                return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
        else:
            super().create(request)


@csrf_exempt
@api_view(['GET'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'Please enter a username and password'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_404_NOT_FOUND)

    token = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)
