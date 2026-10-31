from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using
    either their username or their email address for log in section (not for sign up).
    Would optimally be good if it can be called in specific log in instances, in order to keep
    django authentication backend
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        try:
            lookup = "email__iexact" if "@" in username else "username__iexact"
            user = User._default_manager.filter(**{lookup: username}).first()
            if user is None:
                User().set_password(password)
                return None
        except User.DoesNotExist:
            # Run the default password hasher checking mechanism anyway
            # to protect bad inputs
            User().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
