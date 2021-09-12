from django.conf import settings
from .models import Answer

import uuid


class Anonymous():
    def __init__(self, request):
        self.session = request.session
        self.anonym_user = self.session.get('anonym_user')
        if not self.anonym_user:
            anonym_user = self.session['anonym_user'] = {}
            self.anonym_user = anonym_user
            self.anonym_user['id'] = str(uuid.uuid4().int)[0:10]
            self.anonym_user['answers'] = []

    def add_answers(self, id):
        answer_id = id

        if answer_id not in self.anonym_user['answers']:
            self.anonym_user['answers'].append(id)
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):

        answers_ids = self.anonym_user['answers']
        answers = Answer.objects.filter(id__in=answers_ids)

        anonym_user = self.anonym_user.copy()

        for answer in answers:
            yield answer




