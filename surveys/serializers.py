from rest_framework import serializers

from .models import Survey, Question, Choice, Answer


class BaseSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'
        abstract = True

    def create(self, validated_data):
        try:
            return self.Meta.model.objects.create(**validated_data)
        except:
            raise serializers.ValidationError('"Meta" has not attribute')

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class SurveySerializer(BaseSerializer, serializers.ModelSerializer):
    survey_name = serializers.CharField(max_length=255)
    pub_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    