from __future__ import unicode_literals
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from core.utils import get_avatar_path


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
            Create new user.
        """
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
            Create a new user as SuperUser
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    MARKETING_DIRECTOR = 1
    ART_DIRECTOR = 2
    DESIGNER = 3

    ACCOUNT_TYPE_CHOICES = (
        (MARKETING_DIRECTOR, 'Marketing Director'),
        (ART_DIRECTOR, 'Art Director'),
        (DESIGNER, 'Designer')
    )
    name = models.CharField(max_length=100, verbose_name='Name')
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(verbose_name='Avatar', null=True, blank=True, upload_to=get_avatar_path)
    type = models.IntegerField(verbose_name='Type', choices=ACCOUNT_TYPE_CHOICES, default=3)
    created_at = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return '{0} - {1}'.format(self.name, self.email)

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.get_full_name()

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
