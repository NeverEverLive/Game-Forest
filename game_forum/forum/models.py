import datetime
from time import timezone

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    image = models.ForeignKey('Screenshot', on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey('Genre', on_delete=models.PROTECT, null=True)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'ID {self.id}: {self.title}'


class User(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=30)
    date_register = models.DateField(auto_now_add=True)

    def __str__(self):
        # if self.is_superuser:
        #     return f'ID {self.id}: {self.username}: Superuser'
        # if self.is_staff:
        #     return f'ID {self.id}: {self.username}: Staff'
        return f'ID {self.id}: {self.username}'


# class CustomAccountManager(BaseUserManager):
#
#     def create_user(self, username, password, **other_fields):
#         user = self.model(username=username, **other_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, username, password, **other_fields):
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)
#
#         return self.create_user(username, password, **other_fields)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=30, unique=True)
#     password = models.CharField(max_length=15)
#     date_register = models.DateField(auto_now_add=True)
#     # first_name = models.CharField(max_length=50, null=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#     objects = CustomAccountManager()
#
#     USERNAME_FIELD = 'username'
#     # REQUIRED_FIELDS = ['']


class UserGameRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Awful'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    like = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __init__(self, *args, **kwargs):
        super(UserGameRelation, self).__init__(*args, **kwargs)
        self.old_rate = self.rate

    def __str__(self):
        return f'{self.user.username}: {self.game.title}, RATE {self.rate}'

    def save(self, *args, **kwargs):
        creating = not self.pk

        super().save(*args, **kwargs)

        if self.old_rate != self.rate or creating:
            from forum.logic import set_rating
            set_rating(self.game)


class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class Publisher(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)

    def __str__(self):
        return f'ID {self.id}: Company {self.company.name}, game {self.game.title}'


class Developer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)

    def __str__(self):
        return f'ID {self.id}: Company {self.company.name}, game {self.game.title}'


class Sponsor(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)

    def __str__(self):
        return f'ID {self.id}: Company {self.company.name}, game {self.game.title}'


class Genre(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class Award(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class AwardGameRelation(models.Model):
    award = models.ForeignKey(Award, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'ID {self.id}: Award {self.award.name}, Game {self.game.title}'


class Screenshot(models.Model):
    file = models.ImageField(upload_to='%Y/%m/%d/')
