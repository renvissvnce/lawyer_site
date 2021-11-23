from django.contrib.auth.models import AbstractUser


class EmailBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = AbstractUser.objects.get(email=username)
        except AbstractUser.MultipleObjectsReturned:
            user = AbstractUser.objects.filter(email=username).order_by('id').first()

        except AbstractUser.DoesNotExist:
            return None
        if getattr(user, 'is_active') and user.check_password(password):
            return user
        return None
    def get_user(self,user_id):
        try:
            return AbstractUser.objects.get(pk=user_id)
        except AbstractUser.DoesNotExist:
            return None