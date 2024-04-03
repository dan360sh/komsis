from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class JoinedAccountBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return get_user_model().objects.select_related(
                    "account__cart", "account__favorites").get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
