from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=255)
    pub_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Question(models.Model):
    CHOICES = (
        ('text_answer', 'ответ текстом'),
        ('answer_one_choice', 'ответ с выбором одного варианта'),
        ('multiple_answer', 'ответ с выбором нескольких вариантов')
    )

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    question_type = models.CharField(choices=CHOICES, max_length=255)

    def __str__(self):
        return self.text


class Choice(models.Model):
    CHOICES = (
        ('text_area', 'поле для ввода текста'),
        ('default', 'вариант ответа')
    )
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name='survey', on_delete=models.CASCADE)
    user_id = models.IntegerField()
    choice = models.ForeignKey(Choice, related_name='choice', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.choice_text

