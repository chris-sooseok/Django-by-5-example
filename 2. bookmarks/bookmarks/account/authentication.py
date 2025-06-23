from django.contrib.auth.models import User
from .models import Profile
class EmailAuthBackend:
    """
    Authenticate using an email address.
    """

    # we could use different parameters, but we use username and password to make our backend work with the authentication
    # framework views right away
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def create_profile(backend, user, *args, **kwargs):
    """
    backend: The social auth backend used for user authentication.
    user: The instance of the new or existing user
    Create a user profile for social authentication. This function is added to SOCIAL_AUTH_PIPELINE setting.
    """
    Profile.objects.get_or_create(user=user)
