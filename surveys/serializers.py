from rest_framework import serializers

from .models import Survey, Question, Choice, Answer
from .utils import CurrentUser


class BaseSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'
        abstract = True

    def create(self, validated_data):
        try:
            return self.Meta.model.objects.create(**validated_data)
        except Exception as e:
            print(e)
            raise serializers.ValidationError('"Meta" has not attribute')

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class AnswerSerializer(BaseSerializer, serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(default=CurrentUser())
    survey = serializers.SlugRelatedField(queryset=Survey.objects.all(), slug_field='id')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice = serializers.SlugRelatedField(queryset=Choice.objects.all(), slug_field='id', allow_null=True)
    choice_text = serializers.CharField(max_length=255, allow_null=True, required=False)

    class Meta:
        model = Answer
        fields = '__all__'

    def validate(self, attrs):
        question_type = Question.objects.get(id=attrs['question'].id).question_type
        try:
            if question_type == 'answer_one_choice' or question_type == 'text_answer':
                answer = Answer.objects.get(question=attrs['question'].id,
                                            survey=attrs['survey'].id,
                                            user_id=attrs['user_id'])
            elif question_type == 'multiple_answer':
                answer = Answer.objects.get(question=attrs['question'].id,
                                            survey=attrs['survey'].id,
                                            user_id=attrs['user_id'],
                                            choice=attrs['choice'])
            if answer:
                raise serializers.ValidationError('Answer already exist')
        except Answer.DoesNotExist:
            return attrs


class ChoiceSerializer(BaseSerializer, serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    text = serializers.CharField(max_length=255, allow_null=True)

    def validate(self, attrs):
        try:
            choice = Choice.objects.get(question=attrs['question'].id, text=attrs['text'])
            if choice:
                raise serializers.ValidationError('Choice already exist')
        except Choice.DoesNotExist:
            return attrs

    class Meta:
        model = Choice
        fields = '__all__'

           
class QuestionSerializer(BaseSerializer, serializers.Serializer):
    CHOICES = (
        ('text_answer', 'ответ текстом'),
        ('answer_one_choice', 'ответ с выбором одного варианта'),
        ('multiple_answer', 'ответ с выбором нескольких вариантов')
    )

    id = serializers.IntegerField(read_only=True)
    survey = serializers.SlugRelatedField(queryset=Survey.objects.all(), slug_field='id')
    text = serializers.CharField(max_length=255)
    question_type = serializers.ChoiceField(choices=CHOICES)
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class SurveySerializer(BaseSerializer, serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    pub_date = serializers.DateTimeField(allow_null=True)
    end_date = serializers.DateTimeField()
    description = serializers.CharField(max_length=255)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'