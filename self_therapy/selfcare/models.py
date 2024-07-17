from django.db import models


class Person(models.Model):
    """Persons profile: just minimum."""

    name = models.CharField(
        max_length=256,
        verbose_name='ФИО пользователя',
    )
    tlg_id = models.CharField(
        max_length=256,
        verbose_name='ID диалога пользователя',
    )


class PresetsHelpTips(models.Model):
    """Initial tips for self-help."""

    text = models.TextField(
        verbose_name='Текстовое описание подсказки',
    )


class PersonsHelpTips(models.Model):
    """Help tips for particular person."""

    text = models.TextField(
        verbose_name='Текстовое описание подсказки',
    )
    is_on = models.BooleanField(
        default=True,
        verbose_name='Показывать',
    )
    likeliness = models.DecimalField(
        verbose_name='Рейтинг',
        max_digits=1,
        decimal_places=2,
        default=0.50,
    )
