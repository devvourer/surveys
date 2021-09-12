from django.contrib.auth.models import AnonymousUser
from .anonymous_user import Anonymous


class CurrentUser():

    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id
        if self.user_id is None:
            anonym_user = Anonymous(serializer_field.context['request'])
            print(anonym_user.__dict__)

            self.user_id = anonym_user.anonym_user['id']

    def __call__(self, *args, **kwargs):
        return self.user_id
