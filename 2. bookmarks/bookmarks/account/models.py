from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    # ! extending user model by creating one-to-one relationship
    # ! one-to-one field user will be used to associate profiles with users
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


# ! creating an intermediate model for many-to-many relationship
class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-created'])]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_form} follows {self.user_to}'


# ? add_to_class is used to add an additional field to the model
# ? add_to_class is not a recommended way of adding class, but to keep advantages of User model we do this in this case
# ? symmetrical is one follows one, then, another follows the other
# ? for many-to-many relationships, some of the related manager's methods are disabled, such as add, create, etc.
# ? you need to create or delete instances of the intermediate model instead
user_model = get_user_model()
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False,
    )
)